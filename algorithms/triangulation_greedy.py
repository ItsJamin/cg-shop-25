from instance import Problem, Result
import geometry as geo
import numpy as np
import visualization as vis

def triangulation_greedy(problem : Problem, result : Result):

    all_edges = problem.g_constraints + problem.g_region_boundary.edges
    faces_to_look_at = []

    for e in all_edges:
        for f in [e.face, e.twin.face]:
            if f and geo.is_valid_triangle(f.edge):
                faces_to_look_at.append(f)
                result.step(f, vis.CF_CHECK)

    # create sorted list of points from top to bottom
    points = sort_points_top_down(problem.g_points)

    for index, point in enumerate(points):
        # try to draw edges to each point above
        for prev_point in points[:index]:
            temp_edge = geo.HalfEdge(point, prev_point)          

            if geo.no_edge_intersection(temp_edge, all_edges) and geo.is_edge_in_boundary(temp_edge, problem.g_region_boundary):
                result.g_edges.append(temp_edge)
                all_edges.append(temp_edge)
                f1, f2 = geo.connect_to_grid(temp_edge)

                result.step(temp_edge, color=vis.CL_NORMAL)

                for f in [f1, f2]:
                    if f:
                        if geo.is_non_obtuse_triangle(f):
                            result.step(f, color=vis.CF_VALID)
                        else:
                            # if obtuse triangle, save for later to look at
                            faces_to_look_at.append(f)
                            result.step(f, color=vis.CF_OBUTSE)
    
    return(faces_to_look_at, all_edges, result)


#Helper Functions

def sort_points_top_down(liste : list[geo.Vertex]) -> list[geo.Vertex]:
    """
    Sort list of points from top to bottom (y-axis)
    """

    n = len(liste)
    for i in range(n):
        for j in range(i + 1, n):
            if liste[i].y < liste[j].y:
                liste[i], liste[j] = liste[j], liste[i]
    return liste