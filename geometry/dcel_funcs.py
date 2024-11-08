from .dcel import Vertex, HalfEdge, Face


def create_full_edge(point1 : Vertex, point2 : Vertex):
    """
    Erstellt Zwillings-HalfEdges und gibt Pointer auf den mit Origin p1 zurück.
    """

    edge1 = HalfEdge(point1, point2)
    edge2 = HalfEdge(point2, point1, edge1)

    return edge1,

def connect_edges(edge1, edge2):
    """
    Verlinkt zwei Anliegende Kanten miteinander. Reihenfolge ist wichtig!
    edge1 -> Point -> edge2
    """

    if edge1.twin is None or edge2.twin is None:
        raise Exception("Can't connect unfinished edges. One of the HalfEdges has no twin.")

    if edge1.twin.origin != edge2.origin:
        raise Exception("Second Edge does not start in First Edge's endpoint.")
    
    edge1.next = edge2
    edge2.prev = edge1

    edge1.twin.prev = edge2.twin
    edge2.twin.next = edge1.twin

