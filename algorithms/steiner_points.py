from fractions import Fraction
from instance import Problem, Result
import geometry as geo
import visualization as vis
import numpy as np

def steiner_points(faces_to_look_at, all_edges, problem, result):
    # Fix obtuse triangles by placing Steiner points
    # Handling faces_to_look_at as a stack
    while len(faces_to_look_at) > 0:

        face = faces_to_look_at.pop()

        if not geo.is_non_obtuse_triangle(face):

            if len(face.vertices) == 4:  # should be 4-polygon
                new_faces = divide_trapezoid(face)
                if len(new_faces) > 0:
                    result.g_edges.append(new_faces[0].edge)
                    result.step(new_faces[0].edge, color=vis.CL_NORMAL)
                    for f in new_faces:
                        faces_to_look_at.append(f)
                        result.step(f, color=vis.CF_CHECK)
                else:
                    raise Exception("Wrong Face: ", face._get_edges())
                    result.step(face, color=vis.CF_ERROR)
            elif len(face.vertices) == 3:

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
                    geo.loose_edge(changed_edge)
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
    edge = face.edge
    vertices = [edge.origin, edge.next.origin, edge.next.next.origin]

    angles = []
    for i in range(3):
        v1 = [Fraction(coord) for coord in (vertices[i - 1].position() - vertices[i].position())]
        v2 = [Fraction(coord) for coord in (vertices[(i + 1) % 3].position() - vertices[i].position())]

        dot_product = sum(v1[j] * v2[j] for j in range(len(v1)))
        norm_v1 = Fraction(np.sqrt(float(sum(coord ** 2 for coord in v1))))
        norm_v2 = Fraction(np.sqrt(float(sum(coord ** 2 for coord in v2))))

        angle = Fraction(dot_product) / (norm_v1 * norm_v2)
        angles.append(np.arccos(float(angle)))

    obtuse_index = max(range(3), key=lambda i: angles[i])
    if angles[obtuse_index] <= np.pi / 2:
        return None, None

    A = vertices[obtuse_index]
    B = vertices[(obtuse_index + 1) % 3]
    C = vertices[(obtuse_index + 2) % 3]

    A_pos = [Fraction(coord) for coord in A.position()]
    B_pos = [Fraction(coord) for coord in B.position()]
    C_pos = [Fraction(coord) for coord in C.position()]

    BC_vector = [C_pos[i] - B_pos[i] for i in range(2)]
    BC_length = Fraction(np.sqrt(float(sum(coord ** 2 for coord in BC_vector))))
    BC_unit = [BC_vector[i] / BC_length for i in range(2)]

    projection_length = sum((A_pos[i] - B_pos[i]) * BC_unit[i] for i in range(2))
    projection_point = [B_pos[i] + projection_length * BC_unit[i] for i in range(2)]

    if projection_length < 0:
        steiner_point_position = B_pos
    elif projection_length > BC_length:
        steiner_point_position = C_pos
    else:
        steiner_point_position = projection_point

    changed_edge = [edge for edge in B.edges if edge.twin.origin == C][0]

    return geo.Vertex(float(steiner_point_position[0]), float(steiner_point_position[1])), changed_edge

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

def divide_trapezoid(face: geo.Face) -> list[geo.Face]:
    edges = face.edges
    faces = []

    for edge in edges:
        angle = geo.angle_between_edges(edge.twin, edge.next)

        if np.isclose(angle, 180) or np.isclose(180, 179): #TODO: ???
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
