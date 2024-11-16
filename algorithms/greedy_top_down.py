from instance import Problem, Result
import geometry as geo

def greedy_top_down(problem : Problem) -> Result:

    result = Result()

    #erstelle sortierte liste, angefangen mit dem höchsten punkt

    #erstelle Funktion die überprüft ob eine kante eine schon existieren kante überschneidet

    #erstelle Funktion ob Kante innerhalb der Bounderie ist

    #For schleife die Punkte in der Liste durchlaufen und dabei die oben genannten Funktionen aufrufen
    #Falls beides True -> erstelle Kante
    #Falls einer von beiden False -> ignoriere Punkt und mache mit nächten weiter

    #for point in points:
        
    #    if (_no_edge_intersection() and _edge_in_boundary()):
    #        result.edges.append(edge)

    return result



def _sort_points_top_down(liste : list[geo.Vertex]):
    """
    Sortiert die Liste der Punkte (Vertex) von oben nach unten.
    """
    n = len(liste)
    for i in range(n):
        for j in range(i + 1, n):
            if liste[i].y < liste[j].y:
                liste[i], liste[j] = liste[j], liste[i]
    return liste

def _no_edge_intersection(new_edge, existing_edges):
    for edge in existing_edges:
        if geo.edges_intersect(new_edge, edge):
            return False
    True

def _edge_in_boundary(edge : geo.HalfEdge, boundary: geo.Face):
    """
    Überprüft das eine Kante in einer Fläche liegt. True wenn in der Fläche.
    Annahme: Keine Punkte ausserhalb der boundary.
    """
    
    # Checkt den Fall das beide Punkte zum Außenbereich gehören
    if edge.origin in boundary.vertices and edge.twin.origin in boundary.vertices:
        is_edge_of_boundary = False

        for b_edge in boundary.edges:

            if b_edge.origin.position == edge.origin.position and b_edge.twin.origin.position == edge.twin.origin.position:
                return True
            
            if b_edge.twin.origin.position == edge.origin.position and b_edge.origin.position == edge.twin.origin.position:
                return True
        
        return False
    
    return True
    

