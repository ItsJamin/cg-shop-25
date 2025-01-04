from instance import Problem, Result
import geometry as geo
import numpy as np
import visualization as vis

# TODO:
# 1. punkte auf region boundary setzen: nicht mit rboundary berühren
    # 2. liste an punkte nur auf boundary
    # 3. punkte durch gehen

def triangulation_grid(problem, result):
    all_vertices = problem.g_points
    boundary_edge = problem.g_region_boundary.edges
    points_on_boundary = list({edge.origin for edge in problem.g_region_boundary.edges})

    print("begin", all_vertices)
    print("POINTS ON BOUNDARY",len(points_on_boundary), points_on_boundary)
    #points on region boundary #TODO: while? um für neue punkte
    for edge in boundary_edge:
        for vertex in all_vertices:
            if vertex_hitting_boundary_x(vertex, edge):
                new_point_x = get_vertex_on_boundary_x(vertex, edge)
                if vertex_not_existing(all_vertices, new_point_x):
                    all_vertices = all_vertices + [new_point_x]
                    points_on_boundary.append(new_point_x)
                    result.step(new_point_x, color=vis.CP_STEINER)

    #TODO: neue punkte nicht mit rein
    for edge in boundary_edge:
        for vertex in all_vertices:
            if vertex_hitting_boundary_y(vertex, edge):
                new_point_y = get_vertex_on_boundary_y(vertex, edge)
                if vertex_not_existing(all_vertices, new_point_y):
                    all_vertices = all_vertices + [new_point_y]
                    points_on_boundary.append(new_point_y)
                    result.step(new_point_y, color=vis.CP_STEINER)

    #points in boundary
    print("added", all_vertices)
    print("POINTS ON BOUNDARY",len(points_on_boundary), points_on_boundary)
    all_vertices = sort_points_left_right_bottom_top(all_vertices)
    print("sorted", all_vertices)
    
    temp_vertex = all_vertices

    for vertex in all_vertices:
        temp_vertex.pop(0)

        for next_vertex in temp_vertex:

            if next_vertex in points_on_boundary:
                break

            if vertex.y != next_vertex.y:
                new_point_x = geo.Vertex(next_vertex.x, vertex.y)
                if vertex_not_existing(all_vertices, new_point_x) and geo.is_vertex_in_boundary(new_point_x, problem.g_region_boundary):
                    all_vertices = all_vertices + [new_point_x]
                    result.step(new_point_x, color=vis.CP_STEINER)
            
            if vertex.x != next_vertex.x:
                new_point_y = geo.Vertex(vertex.x, next_vertex.y)
                if vertex_not_existing(all_vertices, new_point_y)and geo.is_vertex_in_boundary(new_point_y, problem.g_region_boundary):
                    all_vertices = all_vertices + [new_point_y]
                    result.step(new_point_y, color=vis.CP_STEINER)
            
            


    return result


#Helper Functions

def vertex_hitting_boundary_x(vertex: geo.Vertex, edge: geo.HalfEdge) -> bool:
    x1, x2 = edge.origin.x, edge.twin.origin.x
    vx = vertex.x

    # Prüfen, ob vx zwischen x1 und x2 liegt
    return min(x1, x2) < vx < max(x1, x2)

def vertex_hitting_boundary_y(vertex: geo.Vertex, edge: geo.HalfEdge) -> bool:
    y1, y2 = edge.origin.y, edge.twin.origin.y
    vy = vertex.y

    # Prüfen, ob vy zwischen y1 und y2 liegt
    return min(y1, y2) < vy < max(y1, y2)

def get_vertex_on_boundary_x(vertex: geo.Vertex, edge: geo.HalfEdge) -> geo.Vertex:
    x = vertex.x
    x1, y1 = edge.origin.x, edge.origin.y
    x2, y2 = edge.twin.origin.x, edge.twin.origin.y

    # Parameter t berechnen
    t = (x - x1) / (x2 - x1)
    # y-Koordinate berechnen
    y = y1 + t * (y2 - y1)

    return geo.Vertex(x, y)

def get_vertex_on_boundary_y(vertex: geo.Vertex, edge: geo.HalfEdge) -> geo.Vertex:
    y = vertex.y
    x1, y1 = edge.origin.x, edge.origin.y
    x2, y2 = edge.twin.origin.x, edge.twin.origin.y

    # Parameter t berechnen
    t = (y - y1) / (y2 - y1)
    # x-Koordinate berechnen
    x = x1 + t * (x2 - x1)

    return geo.Vertex(x, y)

def vertex_not_existing(all_vertices: list[geo.Vertex], vertex: geo.Vertex) -> bool:
    return vertex not in all_vertices

def sort_points_left_right_bottom_top(list : list[geo.Vertex]) -> list[geo.Vertex]:
    n = len(list)

    for i in range(n):
        for j in range(i + 1, n):
            if list[i].y > list[j].y:
                list[i], list[j] = list[j], list[i]

    for i in range(n):
        for j in range(i + 1, n):
            if list[i].x > list[j].x:
                list[i], list[j] = list[j], list[i]
    
    return list