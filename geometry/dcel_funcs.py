from .dcel import Vertex, HalfEdge, Face, edges_intersect
import numpy as np

def connect_edges(edge1 : HalfEdge, edge2 : HalfEdge):
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

def connect_half_edges(edge1 : HalfEdge, edge2 : HalfEdge):
    # TODO: Gucke ob edge1 auf origin edge2 zeigt und edge2 nicht auf edge1
    # dann connecte
    pass


def is_valid_triangle(edge : HalfEdge):

    current_n = edge
    current_p = edge

    for _ in range(3):
        if current_n and current_p:
            current_n = current_n.next
            current_p = current_p.prev
        else:
            return False
    
    return current_n == edge and current_p == edge



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

def connect_to_grid(edge : HalfEdge):

    # Endpoint 
    close_edge, far_edge = get_min_max_angle_edges(edge.twin, edge.twin.origin.edges)

    if close_edge and far_edge:
        edge.next = close_edge
        close_edge.prev = edge

        edge.twin.prev = far_edge.twin
        far_edge.twin.next = edge.twin

    # Origin
    close_edge, far_edge = get_min_max_angle_edges(edge, edge.origin.edges)

    if close_edge and far_edge:
        edge.twin.next = close_edge
        close_edge.prev = edge.twin

        edge.prev = far_edge.twin
        far_edge.twin.next = edge


    if edge not in edge.origin.edges:
        edge.origin.edges.append(edge)
    if edge.twin not in edge.twin.origin.edges:
        edge.twin.origin.edges.append(edge.twin)

    face, face_twin = None, None
    # Create Faces
    if (is_valid_triangle(edge)):
        face = Face(edge)
        print("Face erstellt")
    if (is_valid_triangle(edge.twin)):
        face_twin = Face(edge.twin)
        print("Face erstellt")

    return face, face_twin

def get_min_max_angle_edges(base_edge : HalfEdge, edge_list :list[HalfEdge]) -> tuple[HalfEdge, HalfEdge]:
    """
    Berechnet die Winkel zwischen einer gegebenen HalfEdge und einer Liste von HalfEdges.
    Gibt die Kanten mit dem minimalen und maximalen Winkel zurück.

    Args:
        base_edge (HalfEdge): Die Ausgangskante, deren Winkel zu anderen gemessen werden.
        edge_list (list[HalfEdge]): Eine Liste von HalfEdges, zu denen die Winkel berechnet werden.

    Returns:
        tuple: Ein Tupel (min_edge, max_edge, min_angle, max_angle), wobei
            min_edge die Kante mit dem kleinsten Winkel ist,
            max_edge die Kante mit dem größten Winkel ist,
            min_angle und max_angle die entsprechenden Winkel in Grad sind.
    """
    
    base_dir = base_edge.direction()
    base_dir = base_dir / np.linalg.norm(base_dir)  # Normalisieren
    
    if len(edge_list) == 0:
        return (None,None)

    angles = []
    for edge in edge_list:
        
        edge_dir = edge.direction()
        edge_dir = edge_dir / np.linalg.norm(edge_dir)  # Normalisieren
        
        # Winkel berechnen
        dot_product = np.dot(base_dir, edge_dir)
        cross_product = np.cross(base_dir, edge_dir)
        
        # Winkel in Radiant berechnen und orientiert machen
        angle = np.degrees(np.arctan2(cross_product, dot_product))  # Arctan2 liefert orientierte Winkel

        # Angle in bereich 0 bis 360 cappen
        angle = angle % 360
        angles.append((edge, angle))  # In Grad umwandeln
    
    # Min und Max Winkel finden
    min_edge, min_angle = min(angles, key=lambda x: x[1])
    max_edge, max_angle = max(angles, key=lambda x: x[1])
    
    return (min_edge, max_edge)