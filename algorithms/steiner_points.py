from fractions import Fraction
from instance import Problem, Result
import geometry as geo
import visualization as vis
import numpy as np
import math

def steiner_points(faces_to_look_at, all_edges, problem, result):
    # Fix obtuse triangles by placing Steiner points
    # Handling faces_to_look_at as a stack
    while len(faces_to_look_at) > 0:

        face = faces_to_look_at.pop()

        if not geo.is_non_obtuse_triangle(face):

            if len(face._get_vertices()) == 4:  # should be 4-polygon
                new_faces = divide_steiner_point_quadrangle(face)
                if len(new_faces) > 0:
                    result.g_edges.append(new_faces[0].edge)
                    result.step(new_faces[0].edge, color=vis.CL_NORMAL)
                    for f in new_faces:
                        faces_to_look_at.append(f)
                        result.step(f, color=vis.CF_CHECK)
                else:
                    raise Exception("Wrong Face: ", face._get_edges())
                    result.step(face, color=vis.CF_ERROR)
            elif len(face._get_vertices()) == 3:

                opposite_face, new_faces = _swap_edges(face)
                if len(new_faces) > 0:
                    if opposite_face in faces_to_look_at:
                        faces_to_look_at.remove(opposite_face)
                    result.step(new_faces[0].edge, color=vis.CL_NORMAL)
                    for f in new_faces:
                        if f:
                            faces_to_look_at.append(f)
                            result.step(f, color=vis.CF_CHECK)
                    continue

                print("THIS FACE IS AS FOLLOWS:", face, face.edges)
                steiner_point, changed_edge = calculate_steiner_point(face)
                if steiner_point:               
                    geo.loose_edge(changed_edge) # WRONG
                    if changed_edge in result.g_edges:
                        result.g_edges.remove(changed_edge)
                    result.g_steiner_points.append(steiner_point)
                    result.step(steiner_point, color=vis.CP_STEINER)
                    result.step(changed_edge, color=vis.CL_REMOVE)
                    new_faces = add_steiner_point_to_triangulation(steiner_point, face, all_edges, changed_edge, result)

                    for f in new_faces:
                        faces_to_look_at.append(f)

                    if changed_edge.face in faces_to_look_at:
                        faces_to_look_at.remove(changed_edge.face)
                    if changed_edge.twin.face in faces_to_look_at:
                        faces_to_look_at.remove(changed_edge.twin.face)

        else:
            result.step(face, color=vis.CF_VALID)

    return result

def calculate_steiner_point(face: geo.Face) -> tuple[geo.Vertex, geo.HalfEdge]:
    """
    Berechnet den Steiner-Punkt für ein Dreieck mit einer stumpfen Ecke.

    Parameter:
        face (Face): Ein Dreieck (Face-Objekt) mit genau drei Ecken.

    Rückgabe:
        tuple[Vertex, HalfEdge]:
            - Der neue Vertex (Steiner-Punkt)
            - Die neue Kante (HalfEdge), die den stumpfwinkligen Vertex mit dem Steiner-Punkt verbindet
    """
    if len(face._get_vertices()) != 3:
        raise ValueError("Die Funktion funktioniert nur für Dreiecke.")

    vertices = face._get_vertices()
    edges = face._get_edges()

    # Hilfsfunktion: Berechnung des Kosinus des Winkels an einem Vertex
    def cosine_angle(v1, v2, v3):
        """Berechnet den Kosinus des Winkels bei v2 zwischen v1 und v3 mit Fraction."""
        vec1 = [v1.x - v2.x, v1.y - v2.y]
        vec2 = [v3.x - v2.x, v3.y - v2.y]
        dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
        norm1 = (vec1[0]**2 + vec1[1]**2)
        norm2 = (vec2[0]**2 + vec2[1]**2)
        return dot_product / math.sqrt(norm1 * norm2)

    # Den stumpfwinkligen Vertex finden (Cosinus-Wert < 0)
    obtuse_vertex = None
    opposite_edge = None
    for i in range(3):
        v1 = vertices[i - 1]
        v2 = vertices[i]
        v3 = vertices[(i + 1) % 3]
        if cosine_angle(v1, v2, v3) < 0:
            obtuse_vertex = v2
            opposite_edge = edges[i]
            break

    if obtuse_vertex is None:
        raise ValueError("Das Dreieck hat keinen stumpfen Winkel.")

    # Orthogonale Projektion des stumpfwinkligen Vertex auf die gegenüberliegende Kante
    edge_dir = [
        opposite_edge.twin.origin.x - opposite_edge.origin.x,
        opposite_edge.twin.origin.y - opposite_edge.origin.y
    ]
    edge_origin = [opposite_edge.origin.x, opposite_edge.origin.y]
    obtuse_pos = [obtuse_vertex.x, obtuse_vertex.y]

    # Projektion des Punktes auf die Kante
    t_numerator = (obtuse_pos[0] - edge_origin[0]) * edge_dir[0] + (obtuse_pos[1] - edge_origin[1]) * edge_dir[1]
    t_denominator = edge_dir[0]**2 + edge_dir[1]**2
    t = t_numerator / t_denominator

    projection = [
        edge_origin[0] + t * edge_dir[0],
        edge_origin[1] + t * edge_dir[1]
    ]

    # Neuen Vertex und neue Kante erzeugen
    steiner_vertex = geo.Vertex(float(projection[0]), float(projection[1]))
    
    try:
        steiner_edge = geo.HalfEdge(origin=obtuse_vertex, endpoint=steiner_vertex)
    except:
        print("Steinerpoint an gleicher stelle wie ein Punkt vom Dreieck")
        print(vertices)
        print(steiner_vertex)

    #for point in vertices

    return steiner_vertex, opposite_edge


def add_steiner_point_to_triangulation(steiner_point: geo.Vertex, face: geo.Face, all_edges: list[geo.HalfEdge], changed_edge: geo.HalfEdge, result: Result) -> list[geo.Face]:
    edges = [face.edge, face.edge.next, face.edge.next.next]
    new_edges = []

    for point in [e.origin for e in edges]:
        if Fraction(steiner_point.x) == Fraction(point.x) and Fraction(steiner_point.y) == Fraction(point.y):
            print("Steiner point is already in triangulation")
            return []

    for edge in edges:
        new_edge = geo.HalfEdge(steiner_point, edge.origin)
        geo.connect_to_grid(new_edge)
        all_edges.append(new_edge)
        new_edges.append(new_edge)
        result.g_edges.append(new_edge)
        result.step(new_edge, color=vis.CL_NORMAL)

    return_faces = []
    for edge in new_edges:
        new_face = geo.Face(edge, reference_from_below=True)
        if new_face.is_clockwise():
            result.step(new_face, color=vis.CF_CHECK)
            if len(new_face.vertices) > 3:
                return_faces.insert(0, new_face)
            return_faces.append(new_face)

    return return_faces

def divide_steiner_point_quadrangle(face: geo.Face) -> list[geo.Face]:
    """
    Divides 4-Polygon (triangle with 4-polygon) in two triangles (FOR STEINER POINTS).
    Searches for the steiner point and draws line to opposite point.
    """
    edges = face._get_edges()
    faces = []

    for edge in edges:
        angle = geo.angle_between_edges(edge.twin, edge.next)
        print(angle)

        if np.isclose(angle, 180): #TODO: ???
            print(edge)
            new_edge = geo.HalfEdge(edge.next.origin, edge.next.next.next.origin)
            geo.connect_to_grid(new_edge)

            if new_edge.face:
                faces.append(new_edge.face)
            if new_edge.twin.face:
                faces.append(new_edge.twin.face)
            break

    return faces

def _swap_edges(face: geo.Face) -> tuple[geo.Face, list[geo.Face]]:
    obtuse_edge = geo.get_obtuse_edge(face)

    if not obtuse_edge:
        return None, []

    opposite_face = obtuse_edge.next.twin.face
    opposite_obtuse_edge = obtuse_edge.next.twin.next.next

    if not opposite_face or not opposite_face.is_clockwise() or not geo.is_valid_triangle(opposite_face.edge):
        return opposite_face, []
    if geo.angle_between_edges(opposite_obtuse_edge.prev.twin, opposite_obtuse_edge) <= 90: #TODO:
        return opposite_face, []

    edge_to_remove = obtuse_edge.next
    geo.loose_edge(edge_to_remove)

    edge_to_remove.prev.next = edge_to_remove.twin.next
    edge_to_remove.next.prev = edge_to_remove.twin.prev

    edge_to_remove.twin.prev.next = edge_to_remove.next
    edge_to_remove.twin.next.prev = edge_to_remove.prev

    new_edge = geo.HalfEdge(obtuse_edge.origin, opposite_obtuse_edge.origin)
    face1, face2 = geo.connect_to_grid(new_edge)

    return opposite_face, [face1, face2]
