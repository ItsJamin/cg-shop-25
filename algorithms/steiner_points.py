from fractions import Fraction
from instance import Problem, Result
import geometry as geo
import visualization as vis
import numpy as np
import math
import random
from fractions import Fraction


random.seed(1)

swap_edge = True
def steiner_points(faces_to_look_at, all_edges, problem : Problem, result : Result):
    # Fix obtuse triangles by placing Steiner points
    # Handling faces_to_look_at as a stack
    i = 0
    try:
        while len(faces_to_look_at) > 0:
            i += 1
            face = faces_to_look_at.pop()
            print("--",faces_to_look_at)
            print("--", face)

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
                        result.step(face, color=vis.CF_ERROR)
                        raise Exception(f"Wrong Face (Quadrangle with no 180 degree angle) ({face._get_vertices()})")
                elif len(face._get_vertices()) == 3:
                    if swap_edge and random.random() > 0.4:
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
                    steiner_point, changed_edge = calculate_steiner_point(face)
                    if steiner_point:               
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
            if i < 0:
                vis.show_result(problem, result)
                i = 0
    except Exception as e:
        print(e)
        #vis.show_result(problem, result, show_faces=True)
        tb = e.__traceback__
        while tb:
            print(f"File: {tb.tb_frame.f_code.co_filename}, Line: {tb.tb_lineno}, Function: {tb.tb_frame.f_code.co_name}")
            tb = tb.tb_next
        
    return result

def calculate_steiner_point(face: geo.Face) -> tuple[geo.Vertex, geo.HalfEdge]:
    """
    Berechnet einen Steiner-Punkt für ein Dreieck, indem eine Orthogonale
    von der stumpfen Ecke zur gegenüberliegenden Kante gezogen wird.

    :param face: Ein Dreieck (geo.Face) mit den drei Ecken.
    :return: Der berechnete Steiner-Punkt als geo.Vertex und die gegenüberliegende Kante.
    """

    # Schritt 1: Identifiziere den stumpfen Winkel und die zugehörigen Kanten
    vertices = face._get_vertices()
    edges = face._get_edges()
    assert len(vertices) == 3, "Die Funktion funktioniert nur mit Dreiecken."

    max_angle = 90
    obtuse_vertex = None
    opposite_edge = None

    for edge in edges:
        angle = geo.angle_between_edges(edge.prev.twin, edge)
        if angle > max_angle:
            print("angle", angle, edge.origin)
            max_angle = angle
            obtuse_vertex = edge.origin
            opposite_edge = edge.next

    assert obtuse_vertex is not None and opposite_edge is not None, "Kein stumpfer Winkel gefunden."

    # Schritt 2: Berechne den Schnittpunkt der Orthogonalen mit der gegenüberliegenden Kante
    A = np.array([Fraction(obtuse_vertex.x), Fraction(obtuse_vertex.y)])
    B = np.array([Fraction(opposite_edge.origin.x), Fraction(opposite_edge.origin.y)])
    C = np.array([Fraction(opposite_edge.next.origin.x), Fraction(opposite_edge.next.origin.y)])

    """
    # Richtungsvektor der Kante (B -> C)
    edge_vector = C - B

    # Orthogonale vom Punkt A auf die Kante
    AB = B - A
    AC = C - A

    # Parameter t für den Schnittpunkt auf der Kante (B -> C)
    numerator = -AB @ edge_vector
    denominator = edge_vector @ edge_vector
    assert denominator != 0, "Kante (B, C) ist degeneriert."
    t = numerator / denominator

    # Schnittpunkt berechnen
    intersection = B + t * edge_vector

    # Schritt 3: Rückgabe des Steiner-Punkts und der gegenüberliegenden Kante
    """
    x,y = find_orthogonal_point(A,B,C)
    steiner_vertex = geo.Vertex(x=x, y=y)
    return steiner_vertex, opposite_edge

def add_steiner_point_to_triangulation(steiner_point: geo.Vertex, face: geo.Face, all_edges: list[geo.HalfEdge], changed_edge : geo.HalfEdge, result: Result) -> list[geo.Face]:
    """
    Updates the triangulation to include a Steiner point by splitting the obtuse triangle into smaller triangles.
    """

    geo.loose_edge(changed_edge)

    edges = [face.edge, face.edge.next, face.edge.next.next]
    new_edges = []

    # Check for existing steiner point
    for point in [e.origin for e in edges]:
        if steiner_point.x == point.x and steiner_point.y == point.y:
            return []

    # Create Edges from the Steiner Point to the other points
    for edge in edges:
        new_edge = geo.HalfEdge(edge.origin, steiner_point)
        geo.connect_to_grid(new_edge)
        all_edges.append(new_edge)
        new_edges.append(new_edge)
        result.g_edges.append(new_edge)
        result.step(new_edge, color=vis.CL_NORMAL)  # Visualize the new edge

    # Create new faces for the triangulation
    return_faces = []
    for edge in new_edges:
        try:
            new_face = geo.Face(edge, reference_from_below=True)
        except Exception as e:
            result.step(edge, color=vis.CF_ERROR)
            raise Exception(e)
        if new_face.is_clockwise():
            result.step(new_face, color=vis.CF_CHECK)
            if len(new_face.vertices) > 3: # the trapezoide should be handled first
                return_faces.insert(0, new_face)
            else:
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
            # Triangulate
            new_edge = geo.HalfEdge(edge.next.origin, edge.next.next.next.origin)
            geo.connect_to_grid(new_edge)

            if new_edge.face:
                faces.append(new_edge.face)
            if new_edge.twin.face:
                faces.append(new_edge.twin.face)
            
            if len(faces) < 2:
                raise Exception("Quadrangle not properly divided", faces)


    return faces

def _swap_edges(face: geo.Face) -> tuple[geo.Face, list[geo.Face]]:
    assert geo.is_valid_triangle(face.edge), "face must be triangle for swap edge"
    obtuse_edge = geo.get_obtuse_edge(face)

    if not obtuse_edge:
        return None, []

    opposite_face = obtuse_edge.next.twin.face
    opposite_obtuse_edge = obtuse_edge.next.twin.next.next

    if not opposite_face or not opposite_face.is_clockwise() or not geo.is_valid_triangle(opposite_face.edge):
        return opposite_face, []
    
    # if it is a constraint or boundary, it is not allowed to be swapped.
    if opposite_obtuse_edge.is_constraint:
        return opposite_face, []
    
    # needs exit condition because it would do it infinetly
    if geo.angle_between_edges(opposite_obtuse_edge.prev.twin, opposite_obtuse_edge) <= 90:
        return opposite_face, []

    print("Obtuse Edge 1: ", obtuse_edge)
    print("Obtuse Edge 2: ", opposite_obtuse_edge)


    edge_to_remove = obtuse_edge.next
    geo.loose_edge(edge_to_remove)

    edge_to_remove.prev.next = edge_to_remove.twin.next
    edge_to_remove.next.prev = edge_to_remove.twin.prev

    edge_to_remove.twin.prev.next = edge_to_remove.next
    edge_to_remove.twin.next.prev = edge_to_remove.prev

    current_n = edge_to_remove.next
    current_p = edge_to_remove.next
    for _ in range(4):
        current_n = current_n.next
        current_p = current_p.prev
    
    assert current_n == current_p == edge_to_remove.next, "SwapEdge outer bound is not a valid 4-polygon"

    new_edge = geo.HalfEdge(obtuse_edge.origin, opposite_obtuse_edge.origin)
    face1, face2 = geo.connect_to_grid(new_edge)

    current_n = new_edge
    for i in range(3):
        print(current_n)
        current_n = current_n.next

    faces = list(filter(None,[face1, face2]))

    assert len(faces) == 2, f"Swapping two triangles should give back two triangles, but {len(faces)} was given"

    return opposite_face, faces


def find_orthogonal_point(A, B, C):
    """
    Find the point S on line segment BC such that SA is orthogonal to BC.

    Parameters:
        A (tuple): Coordinates of point A as (x_A, y_A) using Fraction.
        B (tuple): Coordinates of point B as (x_B, y_B) using Fraction.
        C (tuple): Coordinates of point C as (x_C, y_C) using Fraction.

    Returns:
        tuple: Coordinates of point S as (x_S, y_S) using Fraction.
    """
    # Extract coordinates
    x_A, y_A = A
    x_B, y_B = B
    x_C, y_C = C

    # Compute the vector BC and BA
    BC_x = x_C - x_B
    BC_y = y_C - y_B
    BA_x = x_A - x_B
    BA_y = y_A - y_B

    #print("DEBUG: BC vector:", (BC_x, BC_y))
    #print("DEBUG: BA vector:", (BA_x, BA_y))

    # Orthogonality condition: Project BA onto BC
    numerator = BC_x * BA_x + BC_y * BA_y
    denominator = BC_x**2 + BC_y**2

    #print("DEBUG: Numerator (projection):", numerator)
    #print("DEBUG: Denominator (projection length squared):", denominator)

    if denominator == 0:
        raise ValueError("Points B and C cannot be the same.")

    # Solve for t (projection scalar)
    t = Fraction(numerator, denominator)

    #print("DEBUG: Parameter t (projection scalar):", t)

    # Calculate S using t
    x_S = x_B + t * BC_x
    y_S = y_B + t * BC_y

    #print("DEBUG: Calculated S (projected point):", (x_S, y_S))

    # Verify orthogonality by checking dot product of SA and BC
    SA_x = x_A - x_S
    SA_y = y_A - y_S

    #print("DEBUG: SA vector:", (SA_x, SA_y))

    # Dot product
    dot_product = SA_x * BC_x + SA_y * BC_y
    #print("DEBUG: Dot product (should be 0):", dot_product)

    if dot_product != 0:
        raise ValueError("Calculation error: SA is not orthogonal to BC. Check inputs and logic.")

    # Return result as Fractions
    return Fraction(x_S), Fraction(y_S)
