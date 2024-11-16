from instance import Problem, Result
import geometry as geo

def greedy_top_bottom(problem : Problem) -> Result:

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

    pass



def _sort_points_bottom_up():
    pass

def _no_edge_intersection(new_edge, existing_edges):
    for edge in existing_edges:
        if geo.edges_intersect(new_edge, edge):
            return False
    True

def _edge_in_boundary():
    pass