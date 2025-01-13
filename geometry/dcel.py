import numpy as np
from fractions import Fraction

class Vertex:
    def __init__(self, 
                 x: float, 
                 y: float,
                 is_constraint: bool = False):
        """Representation of a point, has references to all outgoing points."""
        self.x = Fraction(x)
        self.y = Fraction(y)
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
    
    def direction(self):
        """Gibt den Richtungsvektor als numpy-Array mit Brüchen zurück."""
        dx = self.twin.origin.x - self.origin.x
        dy = self.twin.origin.y - self.origin.y
        return np.array([dx, dy])

    def length(self):
        """Berechnet die Länge der Kante exakt als Bruch."""
        dx = self.twin.origin.x - self.origin.x
        dy = self.twin.origin.y - self.origin.y
        return (dx**2 + dy**2).sqrt()
    
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
            for edge in result:
                print(edge)
            raise Exception("Face is not closed! Iterating through edges did not end in starting edge.")
        
        return result
    
    def _get_vertices(self) -> list[Vertex]:
        """Gives all vertices of face in cyclical order."""
        return [edge.origin for edge in self._get_edges()]

