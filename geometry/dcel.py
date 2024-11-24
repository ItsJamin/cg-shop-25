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

        if reference_from_below:
            self.set_face_of_edges()
    
    def set_face_of_edges(self):
        for edge in self.get_edges():
                edge.face = self
    
    def get_edges(self) -> list[HalfEdge]:
        """Gives all halfedges that are part of this face."""
        if not self.edge:
            return []
        result = []
        start = self.edge
        current = start
        while True:
            if not current:
                raise Exception("Not closed Face, missing Edges!")

            result.append(current)
            current = current.next
            if current == start:
                break
        
        return result
    
    def get_vertices(self) -> list[Vertex]:
        """Gives all vertices of face in cyclical order."""
        return [edge.origin for edge in self.get_edges()]

    def get_area(self) -> float:
        """Calculates area of face with shoelace formula."""
        vertices = self.get_vertices()
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
        vertices = self.get_vertices()
        n = len(vertices)

        # if less than 3 vertices, it's not a valid polygon
        if n < 3:
            return False

        # create a horizontal line from 'vertex' and count intersection points with the edges
        ray_start = Vertex( float('-inf'), vertex.y)
        ray_end = Vertex(float('inf'), vertex.y)  # infinite in x-direction

        ray_edge = HalfEdge(vertex, ray_end)
        intersect_count = 0

        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]

            # create the HalfEdges for the current edge
            edge = HalfEdge(v1,v2)

            # check if the horizontal line from ray_start to ray_end intersects the edge
            if edges_intersect(edge, ray_edge):
                intersect_count += 1

        # if the number of intersection points is odd, the point is inside
        return intersect_count % 2 == 1


def edges_intersect(edge1 : HalfEdge, edge2 : HalfEdge) -> bool:
    """Checks if two HalfEdges (with twins) intersect."""
    if edge1.origin == edge2.origin:

        if edge1.twin.origin == edge2.twin.origin:
            return True

        return False
    elif  edge1.origin == edge2.twin.origin:

        if edge1.twin.origin == edge2.origin:
            return True

        return False
    elif  edge1.twin.origin == edge2.twin.origin:

        if edge1.origin == edge2.origin:
            return True

        return False
    elif  edge1.twin.origin == edge2.origin:

        if edge1.origin == edge2.twin.origin:
            return True

        return False

    def ccw(a, b, c):
        """
        Checks if the points a, b, c are ordered counterclockwise.

        Parameters:
        a (tuple): The first point.
        b (tuple): The second point.
        c (tuple): The third point.

        Returns:
        bool: True if the points are ordered counterclockwise, False otherwise.
        """
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    p1 = edge1.origin.position()
    p2 = edge1.twin.origin.position() if edge1.twin else None
    q1 = edge2.origin.position()
    q2 = edge2.twin.origin.position() if edge2.twin else None

    if p2 is None or q2 is None:
        raise ValueError("Both HalfEdges need a twin with a defined position.")

    # check if the line segments intersect
    return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))

