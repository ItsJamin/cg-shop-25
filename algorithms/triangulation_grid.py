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
    boundary_edges = problem.g_region_boundary.edges
    points_on_boundary = list({edge.origin for edge in problem.g_region_boundary.edges})

    #TODO: edge in 2 aufteilen bei erstellen von pkt
    all_vertices = sort_points_left_right_bottom_top(all_vertices)
    new_points = []
    for edge in boundary_edges:
        #TODO: edge angucken was aufgeteiltt wurde -> sortiere liste zuerst, damit man immer nur die eine neu erstellte edge angucken muss
        for vertex in all_vertices:
            if vertex_hitting_boundary_x(vertex, edge):
                new_point_x = get_vertex_on_boundary_x(vertex, edge)

                if not geo.is_edge_in_boundary(geo.HalfEdge(vertex,new_point_x), problem.g_region_boundary):
                    continue

                new_edge1, new_edge2 = geo.split_edge_on_point(edge, new_point_x)
                if edge in boundary_edges:
                    boundary_edges.remove(edge)
                boundary_edges.append(new_edge1)
                boundary_edges.append(new_edge2)
                if new_edge1.origin.x > new_edge2.origin.x:
                    edge = new_edge1
                else:
                    edge = new_edge2
                temp_edge = geo.HalfEdge(vertex, new_point_x)

                if geo.no_edge_intersection(temp_edge, boundary_edges) and geo.is_edge_in_boundary(temp_edge, problem.g_region_boundary):
                
                    result.step(temp_edge, color=vis.CL_NORMAL)
                if vertex_not_existing(all_vertices, new_point_x) and vertex_not_existing(new_points, new_point_x):
                    new_points = new_points + [new_point_x]
                    points_on_boundary.append(new_point_x)
                    result.step(new_point_x, color=vis.CP_STEINER)

    for edge in boundary_edges:
        for vertex in all_vertices:
            if vertex_hitting_boundary_y(vertex, edge):
                new_point_y = get_vertex_on_boundary_y(vertex, edge)

                if not geo.is_edge_in_boundary(geo.HalfEdge(vertex,new_point_y), problem.g_region_boundary):
                    continue

                new_edge1, new_edge2 = geo.split_edge_on_point(edge, new_point_y)
                if edge in boundary_edges:
                    boundary_edges.remove(edge)
                boundary_edges.append(new_edge1)
                boundary_edges.append(new_edge2)
                if new_edge1.origin.y > new_edge2.origin.y:
                    edge = new_edge1
                else:
                    edge = new_edge2
                temp_edge = geo.HalfEdge(vertex, new_point_y)
                if geo.no_edge_intersection(temp_edge, boundary_edges):
            
                    result.step(temp_edge, color=vis.CL_NORMAL)
                if vertex_not_existing(all_vertices, new_point_y) and vertex_not_existing(new_points, new_point_y):
                    new_points = new_points + [new_point_y]
                    points_on_boundary.append(new_point_y)
                    result.step(new_point_y, color=vis.CP_STEINER)

    all_vertices = all_vertices + new_points

    #TODO: linien ziehen und eine FKT die kreuzende linien mit ein pkt aufteilt


    #points in boundary
    all_vertices = sort_points_left_right_bottom_top(all_vertices)
    
    temp_vertex = all_vertices.copy()

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