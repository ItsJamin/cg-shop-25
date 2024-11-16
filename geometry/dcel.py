import numpy as np

class Vertex:
    def __init__(self, 
                 x: float, 
                 y: float, 
                 edge : "HalfEdge" = None):
        """Repräsentation eines Punktes, hat eine Referenz zu einer HalfEdge."""
        self.x = x
        self.y = y
        self.edge = edge
    
    def position(self):
        return np.array([self.x, self.y])

    def __repr__(self):
        return f"({self.x}, {self.y})"

class HalfEdge:
    
    def __init__(self, 
                 origin: "Vertex", 
                 twin : "HalfEdge" = None,
                 next : "HalfEdge" = None,
                 prev : "HalfEdge" = None,
                 face : "Face" = None,
                 ):
        """Zwei HalfEdges mit gegensätzlicher Richtung repräsentieren eine Linie. Origin Punkt dient um Richtung darzustellen."""

        self.origin = origin
        if not self.origin.edge:
            self.origin.edge = self

        self.twin = twin
        if self.twin and not twin.twin:
            twin.twin = self
        self.next = next
        self.prev = prev
        self.face = face
    
    def direction(self):
        """Gibt den Richtungsvektor von origin zum Zielknoten zurück."""
        if self.twin:
            return self.twin.origin.position() - self.origin.position()
        return None

    def length(self):
        """Berechnet die euklidische Länge der Kante."""
        return np.linalg.norm(self.direction())
    
    def has_twin(self):
        return self.twin is not None

    def __repr__(self):
        if self.twin:
            return f"({self.origin}) -> ({self.twin.origin})"
        else:
            return f"({self.origin}) -> None"

class Face:
    def __init__(self, edge):
        self.edge = edge
    
    def edges(self) -> list[HalfEdge]:
        """
        Iterator, der alle HalfEdges zurückgibt, die das Face begrenzen.
        """
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
    
    def vertices(self) -> list[Vertex]:
        """
        Gibt alle Eckpunkte des Faces in zyklischer Reihenfolge zurück.
        """
        return [edge.origin for edge in self.edges()]

    def area(self) -> float:
        """
        Berechnet die Fläche des Faces mithilfe der Shoelace-Formel.
        """
        vertices = self.vertices()
        n = len(vertices)
        if n < 3:  # Kein gültiges Polygon
            return 0
        area = 0
        for i in range(n):
            x1, y1 = vertices[i].position()
            x2, y2 = vertices[(i + 1) % n].position()
            area += x1 * y2 - y1 * x2
        return abs(area) / 2