from .dcel import Vertex, HalfEdge, Face, edges_intersect
import numpy as np

def connect_edges(edge1, edge2):
    """
    Verlinkt zwei Anliegende Kanten miteinander. Reihenfolge ist wichtig!
    edge1 -> Point -> edge2
    """

    if not edge1.has_twin() and edge2.has_twin():
        raise Exception("Can't connect unfinished edges. One of the HalfEdges has no twin.")

    if edge1.twin.origin != edge2.origin:
        raise Exception("Second Edge does not start in First Edge's endpoint.")
    
    edge1.next = edge2
    edge2.prev = edge1

    edge1.twin.prev = edge2.twin
    edge2.twin.next = edge1.twin



def is_valid_triangle(edge1, edge2, edge3, existing_edges):
    
    for existing_edge in existing_edges:
        if (edges_intersect(edge1, existing_edge) or 
            edges_intersect(edge2, existing_edge) or 
            edges_intersect(edge3, existing_edge)):
            return False
    
    # Optionally, check if the triangle is within the boundary if needed
    # Example: Use a point-in-polygon test for one vertex or center of triangle
    
    return True



def is_non_obtuse_triangle(edge):
    # Prüft, ob edge und seine Nachbarn existieren und alle Twin-Edges haben
    if edge.has_twin() and edge.next and edge.next.has_twin():
        # Berechne die Richtungsvektoren der Kanten des Dreiecks
        v1 = edge.direction()
        v2 = edge.next.direction()
        v3 = edge.next.next.direction()

        # Berechne die Winkel zwischen den Kantenpaaren
        angle1 = np.arccos(np.dot(v1, -v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        angle2 = np.arccos(np.dot(v2, -v3) / (np.linalg.norm(v2) * np.linalg.norm(v3)))
        angle3 = np.arccos(np.dot(v3, -v1) / (np.linalg.norm(v3) * np.linalg.norm(v1)))
        
        # Prüfe, ob alle Winkel ≤ 90 Grad sind (π/2)
        return all(angle <= np.pi / 2 for angle in [angle1, angle2, angle3])
    
    return False  # Falls kein gültiges Dreieck vorliegt

def add_steiner_point(edge, l: list[Vertex]):
    
    # Setze den Punkt auf die Winkelhalbierende des stumpfen Winkels
    midpoint_x = (edge.origin.x + edge.twin.origin.x) / 2
    midpoint_y = (edge.origin.y + edge.twin.origin.y) / 2
    steiner_point = Vertex(midpoint_x, midpoint_y)
    
    l.append(steiner_point)
    
    return steiner_point

