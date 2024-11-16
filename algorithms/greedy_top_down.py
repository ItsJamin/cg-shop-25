from instance import Problem, Result
import geometry as geo

def greedy_top_down(problem : Problem) -> Result:

    result = Result()

    all_edges = problem.g_constraints + problem.g_region_boundary.edges()

    #erstelle sortierte liste, angefangen mit dem höchsten punkt
    points = _sort_points_top_down(problem.g_points)

    for index, point in enumerate(points):

        for prev_point in points[:index]:
            
            temp_edge = geo.create_full_edge(point, prev_point)
            print(point, prev_point, temp_edge)

            if _no_edge_intersection(temp_edge, all_edges) and _edge_in_boundary(temp_edge, problem.g_region_boundary):
                
                # Edge ist okay
                all_edges.append(temp_edge)
                problem.step(temp_edge, color="orange")
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
            return False
    True

def _edge_in_boundary(edge : geo.HalfEdge, boundary: geo.Face):
    """
    Überprüft das eine Kante in einer Fläche liegt. True wenn in der Fläche.
    Annahme: Keine Punkte ausserhalb der boundary.
    """

    # TODO: Falsch weil linie kann auch innerhalb der boundary sein
    
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
    

