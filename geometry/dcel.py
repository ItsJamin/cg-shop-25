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
                 endpoint : "Vertex" = None
                 ):
        """Zwei HalfEdges mit gegensätzlicher Richtung repräsentieren eine Linie. Origin Punkt dient um Richtung darzustellen."""

        self.origin = origin
        if not self.origin.edge:
            self.origin.edge = self

        self.twin = twin
        if self.twin and not twin.twin:
            twin.twin = self
        elif not self.twin and endpoint:
            self.twin = HalfEdge(endpoint, self)
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
    
    def is_point_in_face(self, vertex : Vertex) -> bool:
        """
        Prüft, ob der Vertex innerhalb des Faces liegt.
        Verwendet den Ray-Casting-Algorithmus und `edges_intersect`-Methode.
        """
        vertices = self.vertices()
        n = len(vertices)

        # Wenn weniger als 3 Ecken, ist es kein gültiges Polygon
        if n < 3:
            return False

        # Erstelle eine horizontale Linie von 'vertex' und zähle Schnittpunkte mit den Kanten
        ray_start = Vertex( float('-inf'), vertex.y)
        ray_end = Vertex(float('inf'), vertex.y)  # Unendlich in x-Richtung

        ray_edge = HalfEdge(vertex, endpoint=ray_end)
        intersect_count = 0

        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]

            # Erstelle die HalfEdges für die aktuelle Kante mit create_full_edge
            edge = HalfEdge(v1,endpoint=v2)
            
            # Überprüfe, ob die horizontale Linie von ray_start bis ray_end die Kante schneidet
            if edges_intersect(edge, ray_edge):
                intersect_count += 1

        # Wenn die Anzahl der Schnittpunkte ungerade ist, liegt der Punkt innerhalb
        return intersect_count % 2 == 1


def edges_intersect(edge1 : HalfEdge, edge2 : HalfEdge):
    """
    Prüft ob zwei HalfEdges (mit twins) sich schneiden.
    """
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

    # TODO: Calculation
    def ccw(a, b, c):
        """
        Prüft, ob die Punkte a, b, c gegen den Uhrzeigersinn angeordnet sind.
        """
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    p1 = edge1.origin.position()
    q1 = edge1.twin.origin.position() if edge1.twin else None
    p2 = edge2.origin.position()
    q2 = edge2.twin.origin.position() if edge2.twin else None

    if q1 is None or q2 is None:
        raise ValueError("Beide HalfEdges benötigen eine Twin-Edge mit einer definierten Position.")

    # Prüfe, ob die Liniensegmente sich schneiden
    return (ccw(p1, p2, q2) != ccw(q1, p2, q2)) and (ccw(p1, q1, p2) != ccw(p1, q1, q2))

