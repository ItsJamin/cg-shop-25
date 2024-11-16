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



def _sort_points_bottom_up(liste):
    n = len(liste)
    for i in range(n):
        for j in range(i + 1, n):
            if liste[i].y < liste[j].y:
                liste[i], liste[j] = liste[j], liste[i]
    return liste

def _no_edge_intersection():
    pass

def _edge_in_boundary():
    pass