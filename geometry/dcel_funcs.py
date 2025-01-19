from .dcel import *

import math

def connect_edges(edge1: HalfEdge, edge2: HalfEdge):
    """
    Links to neighbouring edges together. Order is important!
    edge1 -> Point -> edge2
    """
    if not edge1.has_twin() and edge2.has_twin():
        raise Exception("Can't connect unfinished edges. One of the HalfEdges has no twin.")

    if edge1.twin.origin != edge2.origin:
        print(edge1, edge2)
        raise Exception("Second Edge does not start in First Edge's endpoint.")

    edge1.next = edge2
    edge2.prev = edge1

    edge1.twin.prev = edge2.twin
    edge2.twin.next = edge1.twin

def is_valid_triangle(edge: HalfEdge) -> bool:
    """
    Checks for triangles bei going through the linked edges three times and expecting to be at the start edge.
    """
    current_n = edge
    current_p = edge

    for _ in range(3):
        if current_n and current_p:
            current_n = current_n.next
            current_p = current_p.prev
        else:
            return False

    return current_n == edge and current_p == edge

def is_non_obtuse_triangle(face: Face) -> bool:

    if not is_valid_triangle(face.edge):
        return False

    A = face.edge.origin.position()
    B = face.edge.next.origin.position()
    C = face.edge.next.next.origin.position()

    AB = (B[0] - A[0], B[1] - A[1])
    AC = (C[0] - A[0], C[1] - A[1])
    BC = (C[0] - B[0], C[1] - B[1])
    BA = (A[0] - B[0], A[1] - B[1])
    CA = (A[0] - C[0], A[1] - C[1])
    CB = (B[0] - C[0], B[1] - C[1])

    # Skalares Produkt berechnen
    dot_AB_AC = AB[0] * AC[0] + AB[1] * AC[1]
    dot_BC_BA = BC[0] * BA[0] + BC[1] * BA[1]
    dot_CA_CB = CA[0] * CB[0] + CA[1] * CB[1]

    # Wenn eines der Skalarprodukte negativ ist, hat das Dreieck einen stumpfen Winkel
    return not (dot_AB_AC < 0 or dot_BC_BA < 0 or dot_CA_CB < 0)

    edge = face.edge
    if is_valid_triangle(edge):
        e1 = edge
        e2 = edge.next
        e3 = edge.next.next

        angle1 = angle_between_edges(e1.twin, e2)
        angle2 = angle_between_edges(e2.twin, e3)
        angle3 = angle_between_edges(e3.twin, e1)
        
        # Checks if all anges are ≤ 90 degrees (π/2)
        # Due to computation errors, angle just needs to be close 90 degrees TODO: other method?
        angles = []
        for angle in [angle1, angle2, angle3]:
            
            if np.isclose(angle, 90):
                angles.append(90)
            else:
                angles.append(angle)
        return all(angle <= 90 for angle in angles)
    return False

def get_obtuse_edge(face: Face) -> HalfEdge:
    """
    Returns edge starting from point with obtuse angle (clockwise).
    """
    edge = face.edge
    if is_valid_triangle(edge):
        e1 = edge
        e2 = edge.next
        e3 = edge.next.next

        angle1 = angle_between_edges(e1.twin, e2)
        angle2 = angle_between_edges(e2.twin, e3)
        angle3 = angle_between_edges(e3.twin, e1)

        if angle1 > 90:
            return e2
        if angle2 > 90:
            return e3
        if angle3 > 90:
            return e1

def connect_to_grid(edge : HalfEdge, clockwise = True) -> tuple[Face, Face]:
    """
    Connects a given HalfEdge to a grid by finding the closest and farthest edges from its origin and twin's origin.
    It then updates the next and prev pointers of the HalfEdges to form a closed loop.
    If the HalfEdge is not already in its origin's edges list, it adds it.
    Finally, it creates Faces if the connected edges form valid triangles.

    Parameters:
    edge (HalfEdge): The HalfEdge to connect to the grid.

    Returns:
    tuple[Face, Face]: A tuple containing the created Face objects. If no Face is created, the corresponding value is None.
    """
    # Endpoint 
    close_edge, far_edge = get_min_max_angle_edges(edge.twin, edge.twin.origin.edges)
    if not clockwise:
        close_edge, far_edge = far_edge, close_edge
    

    if close_edge and far_edge:
        edge.next = close_edge
        close_edge.prev = edge

        edge.twin.prev = far_edge.twin
        far_edge.twin.next = edge.twin

    # Origin
    close_edge, far_edge = get_min_max_angle_edges(edge, edge.origin.edges)
    if not clockwise:
        close_edge, far_edge = far_edge, close_edge

    if close_edge and far_edge:
        edge.twin.next = close_edge
        close_edge.prev = edge.twin

        edge.prev = far_edge.twin
        far_edge.twin.next = edge

    # Add HalfEdge to origin's edges list if not already present
    if edge not in edge.origin.edges:
        edge.origin.edges.append(edge)
    if edge.twin not in edge.twin.origin.edges:
        edge.twin.origin.edges.append(edge.twin)

    face, face_twin = None, None
    # Create Faces if connected edges form valid triangles
    if is_valid_triangle(edge):
        face = Face(edge, reference_from_below=True)
    if is_valid_triangle(edge.twin):
        face_twin = Face(edge.twin, reference_from_below=True)

    
    return face, face_twin

def loose_edge(edge: HalfEdge):
    """Uncopples edge from its prev and next and from the points"""
    edge.origin.edges.remove(edge)
    edge.twin.origin.edges.remove(edge.twin)


def get_min_max_angle_edges(base_edge: HalfEdge, edge_list: list[HalfEdge]) -> tuple[HalfEdge, HalfEdge]:
    """
    This function calculates the HalfEdges in the given edge_list that have the smallest and largest angles 
    with respect to the direction of the base_edge.

    Parameters:
    base_edge (HalfEdge): The base HalfEdge to compare the angles with.
    edge_list (list[HalfEdge]): A list of HalfEdges to calculate the angles for.

    Returns:
    tuple[HalfEdge, HalfEdge]: A tuple containing the HalfEdge with the smallest angle (min_edge) and the HalfEdge with the largest angle (max_edge).
    If the edge_list is empty, the function returns (None, None).
    """
    base_dir = base_edge.direction()
    base_dir = (create_fraction(base_dir[0]), create_fraction(base_dir[1]))

    angles = []
    for edge in edge_list:
        edge_dir = edge.direction()
        edge_dir = (create_fraction(edge_dir[0]), create_fraction(edge_dir[1]))

        dot_product = base_dir[0] * edge_dir[0] + base_dir[1] * edge_dir[1]
        cross_product = base_dir[0] * edge_dir[1] - base_dir[1] * edge_dir[0]

        angle = math.degrees(math.atan2(float(cross_product), float(dot_product)))
        angle = angle % 360
        angles.append((edge, angle))

    if not angles:
        return None, None

    min_edge, _ = min(angles, key=lambda x: x[1])
    max_edge, _ = max(angles, key=lambda x: x[1])
    return min_edge, max_edge

def edges_intersect(edge1: HalfEdge, edge2: HalfEdge, on_edge_is_intersection=True) -> bool:
    """
    Determines if two edges (with twins) intersect.
    
    Lines intersects when:
    - they have two common endpoints
    - they have one common endpoint and overlap
    - they cross each other
    - they are on the same line and overlap

    Lines do not intersect when:
    - they have one common endpoint and do not overlap
    - they do not cross and have no common endpoint

    on_edge_is_intersection: If True, edges that end in a point on the other edge (except endpoints) are counted.
    """
    def area(p1, p2, p3):
        return create_fraction(p1[0]) * (p2[1] - p3[1]) + create_fraction(p2[0]) * (p3[1] - p1[1]) + create_fraction(p3[0]) * (p1[1] - p2[1])

    def on_segment(p1, p2, q):
        return (min(p1[0], p2[0]) <= q[0] <= max(p1[0], p2[0]) and
                min(p1[1], p2[1]) <= q[1] <= max(p1[1], p2[1]))

    common_endpoints = count_same_endpoints(edge1, edge2)

    if common_endpoints == 2:
        return True
    elif common_endpoints == 1:
        p1, p2 = edge1.origin.position(), edge1.twin.origin.position()
        p3, p4 = edge2.origin.position(), edge2.twin.origin.position()

        angle_edges = []
        if np.array_equal(p1,p3):
            angle_edges = [edge1, edge2]
        elif np.array_equal(p2,p3):
            angle_edges = [edge1.twin, edge2]
        elif np.array_equal(p1,p4):
            angle_edges = [edge1, edge2.twin]
        else:
            angle_edges = [edge1.twin, edge2.twin]

        angle = angle_between_edges(*angle_edges)
        return angle == 0
    else:
        p1, p2 = edge1.origin.position(), edge1.twin.origin.position()
        p3, p4 = edge2.origin.position(), edge2.twin.origin.position()

        a1 = area(p1, p2, p3)
        a2 = area(p1, p2, p4)
        a3 = area(p3, p4, p1)
        a4 = area(p3, p4, p2)

        if a1 * a2 < 0 and a3 * a4 < 0:
            return True

        if a1 == 0 and on_segment(p1, p2, p3):
            return on_edge_is_intersection
        if a2 == 0 and on_segment(p1, p2, p4):
            return on_edge_is_intersection
        if a3 == 0 and on_segment(p3, p4, p1):
            return on_edge_is_intersection
        if a4 == 0 and on_segment(p3, p4, p2):
            return on_edge_is_intersection

    return False

def no_edge_intersection(new_edge : HalfEdge, existing_edges : list[HalfEdge]) -> bool:
    """
    Checks if an edge intersect with a given array of existing edges
    """
    for edge in existing_edges:
        if edges_intersect(new_edge, edge):
            #print(f"{new_edge} intersects with {edge}")
            return False
    return True

def count_same_endpoints(edge1: HalfEdge, edge2: HalfEdge) -> int:
    """
    Counts how many endpoints two edges share using sets.
    """
    endpoints1 = {tuple(edge1.origin.position()), tuple(edge1.twin.origin.position())}
    endpoints2 = {tuple(edge2.origin.position()), tuple(edge2.twin.origin.position())}
    return len(endpoints1 & endpoints2)



import math

def angle_between_edges(edge1 : HalfEdge, edge2 : HalfEdge):
    """
    Berechnet den Winkel gegen Uhrzeigersinn zwischen zwei Kanten.

    Parameter:
        edge1 (HalfEdge): Die erste Kante.
        edge2 (HalfEdge): Die zweite Kante.

    Rückgabewert:
        float: Der Winkel zwischen den Kanten in Grad, im Uhrzeigersinn.
    """
    # Richtung der Kanten als Vektoren abrufen
    dir1 = edge1.direction().astype(float)
    dir2 = edge2.direction().astype(float)


    # Normalize the direction vectors
    dir1 = dir1 / np.linalg.norm(dir1)
    dir2 = dir2 / np.linalg.norm(dir2)

    # Calculate the dot product and the cross product
    dot_product = np.dot(dir1, dir2)
    cross_product = np.cross(dir1, dir2)

    # Calculate the angle in radians using arctan2 for orientation
    angle = np.degrees(np.arctan2(cross_product, dot_product))  # Arctan2 returns the oriented angle

    # Cap angle in range 0 to 360
    angle = angle % 360#interesting modulo behavior where it needs it two times

    return angle


def is_edge_in_boundary(edge : HalfEdge, face : Face, counter_clockwise : bool = True):
    """
    Checks if an edge is inside the face through a checking angle to edge_faces.
    Assumptions: 
    - No two points are outside the face
    - Face is counter clockwise orientated
    """

    face.vertices = face._get_vertices()
    face.edges = face._get_edges()
    
    points_on_edge = 0
    if edge.origin in face.vertices:
        points_on_edge += 1
    
    if edge.twin.origin in face.vertices:
        points_on_edge += 1
    
    if points_on_edge == 0:
        return True


    boundary_edge = None
    edge_to_add = edge
    for index, e in enumerate(face.edges):
        if edge.origin == e.origin:
            boundary_edge = e
            break
        
        
    
    if not boundary_edge:
        return True
    else:
        # look if new angle is smaller than current angle (should be greater)
        previous_edge = face.edges[index-1].twin
        current_angle = angle_between_edges(previous_edge, boundary_edge)

        if angle_between_edges(previous_edge, edge_to_add) >= current_angle and counter_clockwise:
            return True
        elif angle_between_edges(previous_edge, edge_to_add) <= current_angle and not counter_clockwise:
            return True
        else:
            return False
        
def is_vertex_in_boundary(vertex: Vertex, face: Face) -> bool:
    """
    Checks if a given vertex is within the boundary of a face.

    Parameters:
        vertex (Vertex): The vertex to check.
        face (Face): The face whose boundary is tested.

    Returns:
        bool: True if the vertex is inside the face boundary, False otherwise.
    """
    # Convert the vertex position to a numpy array
    point = vertex.position()

    # Retrieve the vertices of the face in cyclic order
    vertices = face._get_vertices()

    # Use the Ray-Casting algorithm to check if the point is inside the polygon
    n = len(vertices)
    inside = False

    x, y = point

    # Loop through the edges of the face
    for i in range(n):
        v1 = vertices[i].position()
        v2 = vertices[(i + 1) % n].position()

        x1, y1 = v1
        x2, y2 = v2

        # Check if the edge crosses the horizontal ray at y
        if (y1 > y) != (y2 > y):
            # Compute the intersection point of the edge with the ray
            intersection_x = x1 + (x2 - x1) * (y - y1) / (y2 - y1)

            # Check if the point is to the left of the edge (intersection_x > x)
            if x < intersection_x:
                inside = not inside

    return inside

def split_edge_on_point(edge : HalfEdge, split_point : Vertex):
    """
    Precondition: Point is on edge

    Returns two edges, already connected to previous pointers.
    """

    a = edge.origin
    b = edge.twin.origin

    ab_prev = edge.prev
    ab_next = edge.next
    ba_prev = edge.twin.prev
    ba_next = edge.twin.next
    
    first_edge = HalfEdge(a,split_point)
    second_edge = HalfEdge(split_point,b)

    first_edge.next = second_edge
    second_edge.prev = first_edge
    first_edge.twin.prev = second_edge
    second_edge.twin.next = first_edge

    first_edge.prev = ab_prev
    if ab_prev:
        ab_prev.next = first_edge
    first_edge.twin.next = ba_next
    if ba_next:
        ba_next.prev = first_edge.twin

    second_edge.next = ab_next
    if ab_next:
        ab_next.prev = second_edge
    second_edge.twin.prev = ba_prev
    if ba_prev:
        ba_prev.next = second_edge.twin

    return [first_edge, second_edge]