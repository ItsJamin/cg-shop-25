from instance import Problem, Result
import geometry as geo

def greedy_top_down(problem : Problem) -> Result:
    """
    Computes a top down triangulation and afterwards (TODO) fixes obtuse angles.
    """

    result = Result()

    all_edges = problem.g_constraints + problem.g_region_boundary.get_edges()
    faces_to_look_at = []

    # create sorted list of points from top to bottom
    points = _sort_points_top_down(problem.g_points)

    for index, point in enumerate(points):

        print(index, point.position())

        for prev_point in points[:index]:

            print("--Looks at PrevPoint: ", prev_point.position())           
            temp_edge = geo.HalfEdge(point, prev_point)          

            if _no_edge_intersection(temp_edge, all_edges) and _edge_in_boundary(temp_edge, problem.g_region_boundary):
                
                print("--Edge okay, adding it...")
                
                all_edges.append(temp_edge)
                geo.connect_to_grid(temp_edge)

                result.step(temp_edge, color="orange")

                for f in [temp_edge.face, temp_edge.twin.face]:
                    if f:
                        if geo.is_non_obtuse_triangle(f):
                            result.step(f, color="#BCD8B7")
                        else:
                            # if obtuse triangle, save for later to look at
                            faces_to_look_at.append(f)
                            result.step(f, color="#ffc1cc")
    
    for face in faces_to_look_at:
        # TODO: removing obtuse triangles
        pass

    return result


# Helping Functions #

def _sort_points_top_down(liste : list[geo.Vertex]) -> list[geo.Vertex]:
    """
    Sort list of points from top to bottom (y-axis)
    """
    n = len(liste)
    for i in range(n):
        for j in range(i + 1, n):
            if liste[i].y < liste[j].y:
                liste[i], liste[j] = liste[j], liste[i]
    return liste

def _no_edge_intersection(new_edge : geo.HalfEdge, existing_edges : list[geo.HalfEdge]) -> bool:
    """
    Checks if an edge intersect with a given array of existing edges
    """
    for edge in existing_edges:
        if geo.edges_intersect(new_edge, edge):
            print(f"{new_edge} intersects with {edge}")
            return False
    return True

def _edge_in_boundary(edge : geo.HalfEdge, boundary: geo.Face) -> bool:
    """
    Checks if an edge is inside the boundary through checking if the middle point would be inside the boundary.
    """
    middle = geo.Vertex(*((edge.twin.origin.position() + edge.origin.position())/2))

    return boundary.is_point_in_face(middle)
