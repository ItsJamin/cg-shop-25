from instance import Problem, Result
import geometry as geo
import numpy as np
import visualization as vis

def steiner_points(faces_to_look_at, all_edges, problem, result):
    # Fix obtuse triangles by placing Steiner points
    # Handling faces_to_look_at as a stack
    while len(faces_to_look_at) > 0:

        face = faces_to_look_at.pop()
        #print("Next Face: ", face)

        if not geo.is_non_obtuse_triangle(face):

            if len(face.vertices) == 4: #should be 4-polygon
                new_faces = divide_trapezoid(face)
                if len(new_faces) > 0:
                    result.step(new_faces[0].edge, color=vis.CL_NORMAL)
                    for f in new_faces:
                        faces_to_look_at.append(f)
                        result.step(f, color=vis.CF_CHECK)
                    faces_to_look_at.remove(face)
                else:
                    print("WRONG FACE ", face)
                    result.step(face, color=vis.CF_ERROR)
            elif len(face.vertices) == 3:

                #TODO: try switching inner edge with other triangles

                steiner_point, changed_edge = calculate_steiner_point(face)
                if steiner_point:
                    geo.loose_edge(changed_edge)
                    #print("Adding Steiner point on edge: ", changed_edge)
                    problem.g_points.append(steiner_point) #TODO: save elsewhere (result, extra steiner pointsl ist)
                    result.step(steiner_point, color=vis.CP_STEINER)  # visualize the steiner point
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
    Berechnet einen Steiner-Punkt für ein Dreieck, indem ein rechter Winkel
    von der stumpfen Ecke zur gegenüberliegenden Kante hergestellt wird.

    :param face: Ein Dreieck (geo.Face) mit den drei Ecken.
    :return: Der berechnete Steiner-Punkt als geo.Vertex.
    """
    edge = face.edge
    vertices = [edge.origin, edge.next.origin, edge.next.next.origin]

    # Finde den Punkt mit dem stumpfen Winkel
    angles = []
    for i in range(3):
        v1 = vertices[i - 1].position() - vertices[i].position()
        v2 = vertices[(i + 1) % 3].position() - vertices[i].position()
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        angles.append(angle)

    obtuse_index = max(range(3), key=lambda i: angles[i])
    if angles[obtuse_index] <= np.pi / 2:
        return None, None  # Kein stumpfer Winkel

    # Definiere die Punkte
    A = vertices[obtuse_index]  # Stumpfer Winkel
    B = vertices[(obtuse_index + 1) % 3]  # Erste Ecke der gegenüberliegenden Kante
    C = vertices[(obtuse_index + 2) % 3]  # Zweite Ecke der gegenüberliegenden Kante

    # Positionen der Punkte
    A_pos = A.position()
    B_pos = B.position()
    C_pos = C.position()

    # Richtung und Länge der Kante B -> C
    BC_vector = C_pos - B_pos
    BC_length = np.linalg.norm(BC_vector)
    BC_unit = BC_vector / BC_length  # Einheitsvektor

    # Orthogonale Projektion von A auf die Kante B -> C
    projection_length = np.dot(A_pos - B_pos, BC_unit)
    projection_point = B_pos + projection_length * BC_unit

    # Sicherstellen, dass der Steiner-Punkt auf der Kante liegt
    if projection_length < 0:  # Vor dem Punkt B
        steiner_point_position = B_pos
    elif projection_length > BC_length:  # Nach dem Punkt C
        steiner_point_position = C_pos
    else:  # Innerhalb der Kante
        steiner_point_position = projection_point

    # Finde kante von B nach C
    changed_edge = [edge for edge in B.edges if edge.twin.origin == C][0]

    return geo.Vertex(steiner_point_position[0], steiner_point_position[1]), changed_edge


def add_steiner_point_to_triangulation(steiner_point: geo.Vertex, face: geo.Face, all_edges: list[geo.HalfEdge], changed_edge : geo.HalfEdge, result: Result) -> list[geo.Face]:
    """
    Updates the triangulation to include a Steiner point by splitting the obtuse triangle into smaller triangles.
    """

    edges = [face.edge, face.edge.next, face.edge.next.next]
    new_edges = []

    #print("Kanten des Dreiecks wo Steinerpunkt hinzugefügt wird", edges)
    for edge in edges:
        new_edge = geo.HalfEdge(steiner_point, edge.origin)
        geo.connect_to_grid(new_edge)
        all_edges.append(new_edge)
        new_edges.append(new_edge)
        result.step(new_edge, color=vis.CL_NORMAL)  # Visualize the new edge

    # Create new faces for the triangulation
    return_faces = []
    for edge in new_edges:
        #if geo.is_valid_triangle(edge):
        #print(edge, edge.next, edge.next.next)
        new_face = geo.Face(edge, reference_from_below=True)
        if new_face.is_clockwise():
            result.step(new_face, color=vis.CF_CHECK)
            if len(new_face.vertices) > 3: # the trapezoide should be handled first
                return_faces.insert(0, new_face)
            return_faces.append(new_face)

    #TODO: Gib die Faces um den neuen Steiner Punkt Zurück 
    return return_faces

def divide_trapezoid(face : geo.Face) -> list[geo.Face]:
    """Divides a trapezoid into two triangles"""
    # TODO: make better division
    #print(face)
    edges = face.edges
    faces = []
    
    for edge in edges:
        angle = geo.angle_between_edges(edge.twin, edge.next)

        if np.isclose(angle, 180) or np.isclose(180, 179):
            new_edge = geo.HalfEdge(edge.next.origin, edge.next.next.next.origin)
            geo.connect_to_grid(new_edge)

            if new_edge.face:
                faces.append(new_edge.face)
            if new_edge.twin.face:
                faces.append(new_edge.twin.face)
            break
    
    return faces