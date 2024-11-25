from instance import Problem, Result
import geometry as geo
import numpy as np

def greedy_top_down(problem: Problem) -> Result:
    """
    Computes a top-down triangulation and fixes obtuse angles by placing Steiner points.
    """
    result = Result()

    all_edges = problem.g_constraints + problem.g_region_boundary.edges
    faces_to_look_at = []

    # create sorted list of points from top to bottom
    points = _sort_points_top_down(problem.g_points)

    for index, point in enumerate(points):
        #print(index, point.position())

        for prev_point in points[:index]:
            #print("--Looks at PrevPoint: ", prev_point.position())           
            temp_edge = geo.HalfEdge(point, prev_point)          

            if _no_edge_intersection(temp_edge, all_edges) and _edge_in_boundary(temp_edge, problem.g_region_boundary):
                #print("--Edge okay, adding it...")
                #print(temp_edge)
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
            else:
                pass#print("Not taking ", temp_edge)
                
    # Fix obtuse triangles by placing Steiner points
    j = 0
    #for i, face in enumerate(faces_to_look_at):

    # Handling faces_to_look_at as a stack
    while len(faces_to_look_at) > 0:

        face = faces_to_look_at.pop()
        print("Next Face: ", face)
        if not geo.is_non_obtuse_triangle(face):
            if len(face.vertices) > 3:
                # TODO: wenn kein Dreieck, trianguliere
                continue

            #TODO: Schaue nach ob Kanten Tausch möglich um Steiner Punkte zu reduzieren
            steiner_point, changed_edge = _calculate_steiner_point(face)
            

            if steiner_point:
                geo.loose_edge(changed_edge)
                print("Adding Steiner point on edge: ", changed_edge)
                problem.g_points.append(steiner_point) #wahrshcienlich eher bei result
                result.step(steiner_point, color="red")  # Visualize the Steiner point
                result.step(changed_edge, color="white")
                new_faces = _add_steiner_point_to_triangulation(steiner_point, face, all_edges, changed_edge, result)
                for f in new_faces:
                    faces_to_look_at.append(f)
                
                if changed_edge.face in faces_to_look_at:
                    faces_to_look_at.remove(changed_edge.face)
                if changed_edge.twin.face in faces_to_look_at:
                    faces_to_look_at.remove(changed_edge.twin.face)
                
                j+=1
                #if j == 10:
                #    return result
        else:
            result.step(face, color="#BCD8B7")
        
                    

    return result

# Helper Functions 

def _calculate_steiner_point(face: geo.Face) -> tuple[geo.Vertex, geo.HalfEdge]:
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




def _add_steiner_point_to_triangulation(steiner_point: geo.Vertex, face: geo.Face, all_edges: list[geo.HalfEdge], changed_edge : geo.HalfEdge, result: Result) -> list[geo.Face]:
    """
    Updates the triangulation to include a Steiner point by splitting the obtuse triangle into smaller triangles.
    """

    edges = [face.edge, face.edge.next, face.edge.next.next]
    new_edges = []

    print("Kanten des Dreiecks wo Steinerpunkt hinzugefügt wird", edges)
    for edge in edges:
        new_edge = geo.HalfEdge(steiner_point, edge.origin)
        geo.connect_to_grid(new_edge)
        all_edges.append(new_edge)
        new_edges.append(new_edge)
        result.step(new_edge, color="green")  # Visualize the new edge

    # Create new faces for the triangulation
    return_faces = []
    for edge in new_edges:
        #if geo.is_valid_triangle(edge):
        print(edge, edge.next, edge.next.next)
        new_face = geo.Face(edge, reference_from_below=True)
        if new_face.is_clockwise():
            result.step(new_face, color="#ADADFF")
            return_faces.append(new_face)

    #TODO: Gib die Faces um den neuen Steiner Punkt Zurück 
    return return_faces

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