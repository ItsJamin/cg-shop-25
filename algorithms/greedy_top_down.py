from instance import Problem, Result
import geometry as geo

def greedy_top_down(problem : Problem) -> Result:

    result = Result()

    all_edges = problem.g_constraints + problem.g_region_boundary.edges()

    #erstelle sortierte liste, angefangen mit dem höchsten punkt
    points = _sort_points_top_down(problem.g_points)

    print(points)

    for index, point in enumerate(points):

        print(index, point.position())

        for prev_point in points[:index]:

            print("--Schaut auf ", prev_point.position())
            
            temp_edge = geo.HalfEdge(point, prev_point)
            

            if _no_edge_intersection(temp_edge, all_edges) and _edge_in_boundary(temp_edge, problem.g_region_boundary):
                
                print("Edge okay")

                # Edge ist okay
                all_edges.append(temp_edge)
                result.step(temp_edge, color="orange")
                # TODO: verkettung der edge mit dem rest.
            

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

def _no_edge_intersection(new_edge : geo.HalfEdge, existing_edges : list[geo.HalfEdge]):
    """
    Überprüft ob eine neue Kante mit bereits existierenden Kanten sich überschneiden.
    """
    for edge in existing_edges:
        if geo.edges_intersect(new_edge, edge):
            print("Intersektion mit ", edge)
            return False
    return True

def _edge_in_boundary(edge : geo.HalfEdge, boundary: geo.Face):
    """
    Überprüft das eine Kante in einer Fläche liegt. True wenn in der Fläche.
    """
    print("Nicht in boundary")
    middle = geo.Vertex(*((edge.twin.origin.position() + edge.origin.position())/2))
    print(middle)

    return boundary.is_point_in_face(middle)
    

