import numpy as np

class Vertex:
    def __init__(self, 
                 x: float, 
                 y: float,
                 is_constraint: bool = False):
        """Representation of a point, has references to all outgoing points."""
        self.x = x
        self.y = y
        self.edges = []
        self.is_constraint = is_constraint

    def position(self):
        return np.array([self.x, self.y])

    def __repr__(self):
        return f"({self.x}, {self.y})"

class HalfEdge:
    
    def __init__(self, 
                 origin: "Vertex", 
                 endpoint : "Vertex" = None,
                 twin : "HalfEdge" = None,
                 next : "HalfEdge" = None,
                 prev : "HalfEdge" = None,
                 face : "Face" = None,
                 reference_from_below: bool = False,
                 is_constraint: bool = False
                 ):
        """
        Two HalfEdges represent a single edge. The direction of a HalfEdge is determined by the origin.

        twin oder endpoint has to be set for a full functional edge!

        reference_from_below: If True, adds a reference from the points to the HalfEdges.
        -> This is wanted when the edge is not temporary and should be added to the grid.
        """

        self.origin = origin
        if reference_from_below:
            self.origin.edges.append(self)

        self.twin = twin
        if self.twin and not twin.twin:
            twin.twin = self
        elif not self.twin and endpoint:
            if all([i == j for i, j in zip(origin.position(), endpoint.position())]):
                raise Exception("HalfEdge darf nicht auf gleichen Punkt zeigen", origin.position(), endpoint.position())
            self.twin = HalfEdge(endpoint, twin=self, reference_from_below=reference_from_below)
        self.next = next
        self.prev = prev
        self.face = face
        self.is_constraint = is_constraint

        if not self.twin:
            raise Warning("HalfEdge ohne Zwilling definiert.")
    
    def direction(self) -> np.ndarray:
        """Returns the direction vector from the origin to the endpoint."""
        return self.twin.origin.position() - self.origin.position()

    def length(self) -> float:
        """Calculates the Euclidean length of the edge."""
        return np.linalg.norm(self.direction())
    
    def has_twin(self):
        return self.twin is not None

    def __repr__(self):
        if self.twin:
            return f"({self.origin}) -> ({self.twin.origin})"
        else:
            return f"({self.origin}) -> None"

class Face:
    def __init__(self, edge : HalfEdge, reference_from_below : bool = False):
        """
        edge: An edge of the face
        reference_from_below: If true sets the facepointer of all halfedges to this face.
        -> Wanted if face is not temporary and should be part of the grid.
        """
        self.edge = edge
        self.edges = self._get_edges()
        self.vertices = self._get_vertices()

        if reference_from_below:
            self.set_face_of_edges()
    

    def is_clockwise(self) -> bool:
        """
        Determines if the edges of a face are iterated in a clockwise direction.

        Parameters:
            face (Face): The face object containing a reference to one of its half-edges.

        Returns:
            bool: True if the edges are iterated clockwise, False otherwise.
        """
        # Start from an arbitrary half-edge of the face
        
        start_edge = self.edge
        edge = start_edge

        # Initialize the signed area
        signed_area = 0

        # Iterate through the edges of the face
        while True:
            # Get the origin and destination vertices of the edge
            origin = edge.origin
            destination = edge.twin.origin

            # Add the contribution to the signed area
            signed_area += (origin.x * destination.y - origin.y * destination.x)

            # Move to the next edge
            edge = edge.next

            # Stop if we are back at the starting edge
            if edge == start_edge:
                break

        # Determine the orientation based on the signed area
        return signed_area < 0  # Negative signed area means clockwise


    def __repr__(self):
        return f"[{self.vertices}]"

    def set_face_of_edges(self):
        for edge in self._get_edges():
                edge.face = self
    
    def _get_edges(self) -> list[HalfEdge]:
        """Gives all HalfEdges that are part of this face."""
        if not self.edge:
            return []
        result = []
        start = self.edge
        current = start

        while current not in result:
            result.append(current)
            current = current.next
        
        if current != start:
            raise Exception("Face is not closed! Iterating through edges did not end in starting edge.")
        
        return result
    
    def _get_vertices(self) -> list[Vertex]:
        """Gives all vertices of face in cyclical order."""
        return [edge.origin for edge in self._get_edges()]

    def get_area(self) -> float:
        """Calculates area of face with shoelace formula."""
        vertices = self._get_vertices()
        n = len(vertices)
        if n < 3:  # no valid polygon
            return 0
        area = 0
        for i in range(n):
            x1, y1 = vertices[i].position()
            x2, y2 = vertices[(i + 1) % n].position()
            area += x1 * y2 - y1 * x2
        return abs(area) / 2
    
    
    def is_point_in_face(self, vertex : Vertex) -> bool:
        """
        Check if a given vertex is inside the face.
        Uses the Ray-Casting algorithm and the `edges_intersect` method.
        """
        edges = self.edges#_get_edges()

        # if less than 3 vertices, it's not a valid polygon
        if len(edges) < 3:
            print("No polygon", len(edges))
            return False

        # create a horizontal line from 'vertex' and count intersection points with the edges
        # "infinite" in x-direction
        # infinity not possible due to area calculations so just over max x as replacement
        ray_end_x = Vertex(max(self.vertices, key=lambda v: v.x).x+1, vertex.y)  
        ray_end_y = Vertex(max(self.vertices, key=lambda v: v.y).y+1, vertex.y)

        ray_edge_horizontal = HalfEdge(vertex, ray_end_x)
        ray_edge_vertical = HalfEdge(vertex, ray_end_y)

        intersect_count = 0

        for edge in edges:

            # check if the horizontal line from ray_start to ray_end intersects the edge
            if edges_intersect(edge, ray_edge_horizontal) or edges_intersect(edge, ray_edge_vertical):
                print(f"{vertex}-Ray goes through {edge}")
                intersect_count += 1

        # if the number of intersection points is odd, the point is inside
        print(intersect_count)
        return intersect_count % 2 == 1


def edges_intersect(edge1: HalfEdge, edge2: HalfEdge) -> bool:
    """
    Determines if two edges (with twins) intersect.
    
    Lines intersects when:
    - they have two common endpoints
    - they have one common endpoint and overlap
    - they cross each other
    - they are on the same line and overlap

    Lines do not intersect when:
    - they have one common endpoint and do not overlap
    - they do not cross and have no common endpoint
    """

    def area(p1, p2, p3):
        """Calculates the signed area of the triangle formed by three points."""
        return 0.5 * ((p1[0] * (p2[1] - p3[1]) +
                       p2[0] * (p3[1] - p1[1]) +
                       p3[0] * (p1[1] - p2[1])))

    common_endpoints = count_same_endpoints(edge1, edge2)

    if common_endpoints == 2:
        #print("||| Have same points")
        return True
    elif common_endpoints == 1:
        # TODO: check for collinearity
        p1 = edge1.origin.position()
        p2 = edge1.twin.origin.position()
        p3 = edge2.origin.position()
        p4 = edge2.twin.origin.position()

        # Find the two edges that need to be looked at from the common point
        angle_edges = []
        if np.array_equal(p1, p3):
            angle_edges = [edge1, edge2]
        elif np.array_equal(p2, p3):
            angle_edges = [edge1.twin, edge2]
        elif np.array_equal(p1, p4):
            angle_edges = [edge1, edge2.twin]
        else: # has to be p2, p4
            angle_edges = [edge1.twin, edge2.twin]
        
        angle = angle_between_edges(*angle_edges)
        #print(f"||| Have ome point in common and angle is, ", angle)
        if angle == 0:
            return True
        else:
            return False
            

    else:
        # Check if lines intersect (using area method)
        p1 = edge1.origin.position()
        p2 = edge1.twin.origin.position()
        p3 = edge2.origin.position()
        p4 = edge2.twin.origin.position()

        # Calculate areas
        a1 = area(p1, p2, p3)
        a2 = area(p1, p2, p4)
        a3 = area(p3, p4, p1)
        a4 = area(p3, p4, p2)

        # Check if areas have opposite signs
        if a1 * a2 <= 0 and a3 * a4 <= 0:
            return True
        
        #print("|||Have no points and common and do not intersect")

        # Check for collinear overlap
        #if np.isclose(a1, 0) or np.isclose(a2, 0) or np.isclose(a3, 0) or np.isclose(a4, 0):
        #    # TODO: Check if collinear segments overlap
        #    pass

    return False

def count_same_endpoints(edge1: HalfEdge, edge2: HalfEdge) -> int:
    """
    Counts how many endpoints two edges share using sets.
    """
    endpoints1 = {tuple(edge1.origin.position()), tuple(edge1.twin.origin.position())}
    endpoints2 = {tuple(edge2.origin.position()), tuple(edge2.twin.origin.position())}
    return len(endpoints1 & endpoints2)

import numpy as np

def angle_between_edges(edge1: HalfEdge, edge2: HalfEdge) -> float:
    """
    Calculates the angle (in degrees) between two edges.

    Parameters:
        edge1 (HalfEdge): The first edge.
        edge2 (HalfEdge): The second edge.

    Returns:
        float: The angle between the two edges in degrees.
    """
    # Direction vectors of the two edges
    dir1 = edge1.direction()
    dir2 = edge2.direction()

    # Normalize the direction vectors
    dir1 = dir1 / np.linalg.norm(dir1)
    dir2 = dir2 / np.linalg.norm(dir2)

    # Calculate the dot product and the cross product
    dot_product = np.dot(dir1, dir2)
    cross_product = np.cross(dir1, dir2)

    # Calculate the angle in radians using arctan2 for orientation
    angle = np.degrees(np.arctan2(cross_product, dot_product))  # Arctan2 returns the oriented angle

    # Cap angle in range 0 to 360
    angle = angle % 360

    return angle
