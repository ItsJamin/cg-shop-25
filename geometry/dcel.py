import numpy as np

class Vertex:
    def __init__(self, 
                 x: float, 
                 y: float,
                 is_constraint: bool = False):
        """Repräsentation eines Punktes, hat eine Referenz zu einer HalfEdge."""
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
                 point_reference: bool = False,
                 is_constraint: bool = False
                 ):
        """
        Zwei HalfEdges mit gegensätzlicher Richtung repräsentieren eine Linie. Origin Punkt dient um Richtung darzustellen.

        `twin` oder `endpoint` muss gesetzt sein, um eine volle Kante zu setzen.

        point_reference: Wenn True addet die Kante direkt zu den Zeigern vom Punkt
        -> Nur gewollt wenn man sicher ist das man Kante hinzufügen will.
        """

        self.origin = origin
        if point_reference:
            self.origin.edges.append(self)

        self.twin = twin
        if self.twin and not twin.twin:
            twin.twin = self
        elif not self.twin and endpoint:
            self.twin = HalfEdge(endpoint, twin=self, point_reference=point_reference)
        self.next = next
        self.prev = prev
        self.face = face
        self.is_constraint = is_constraint

        if not self.twin:
            raise Warning("HalfEdge ohne Zwilling definiert.")
    
    def direction(self):
        """Gibt den Richtungsvektor von origin zum Zielknoten zurück."""
        return self.twin.origin.position() - self.origin.position()

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
    def __init__(self, edge : HalfEdge):
        self.edge = edge

        for edge in self.get_edges():
            edge.face = self
    
    def get_edges(self) -> list[HalfEdge]:
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
    
    def get_vertices(self) -> list[Vertex]:
        """
        Gibt alle Eckpunkte des Faces in zyklischer Reihenfolge zurück.
        """
        return [edge.origin for edge in self.get_edges()]

    def get_area(self) -> float:
        """
        Berechnet die Fläche des Faces mithilfe der Shoelace-Formel.
        """
        vertices = self.get_vertices()
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
        vertices = self.get_vertices()
        n = len(vertices)

        # Wenn weniger als 3 Ecken, ist es kein gültiges Polygon
        if n < 3:
            return False

        # Erstelle eine horizontale Linie von 'vertex' und zähle Schnittpunkte mit den Kanten
        ray_start = Vertex( float('-inf'), vertex.y)
        ray_end = Vertex(float('inf'), vertex.y)  # Unendlich in x-Richtung

        ray_edge = HalfEdge(vertex, ray_end)
        intersect_count = 0

        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]

            # Erstelle die HalfEdges für die aktuelle Kante
            edge = HalfEdge(v1,v2)
            
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

    def ccw(a, b, c):
        """
        Prüft, ob die Punkte a, b, c gegen den Uhrzeigersinn angeordnet sind.
        """
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    p1 = edge1.origin.position()
    p2 = edge1.twin.origin.position() if edge1.twin else None
    q1 = edge2.origin.position()
    q2 = edge2.twin.origin.position() if edge2.twin else None

    if p2 is None or q2 is None:
        raise ValueError("Beide HalfEdges benötigen eine Twin-Edge mit einer definierten Position.")

    # Prüfe, ob die Liniensegmente sich schneiden
    return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))

