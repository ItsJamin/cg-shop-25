from .dcel import *
import numpy as np

def connect_edges(edge1 : HalfEdge, edge2 : HalfEdge):
    """
    Links to neighbouring edges together. Order is important!
    edge1 -> Point -> edge2
    """

    if not edge1.has_twin() and edge2.has_twin():
        raise Exception("Can't connect unfinished edges. One of the HalfEdges has no twin.")

    if edge1.twin.origin != edge2.origin:
        raise Exception("Second Edge does not start in First Edge's endpoint.")
    
    edge1.next = edge2
    edge2.prev = edge1

    edge1.twin.prev = edge2.twin
    edge2.twin.next = edge1.twin

def is_valid_triangle(edge : HalfEdge) -> bool:
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


def is_non_obtuse_triangle(face : Face) -> bool:
    
    edge = face.edge
    if is_valid_triangle(edge): 
        e1 = edge
        e2 = edge.next
        e3 = edge.next.next

        #angle1 = np.arccos(np.dot(v1, -v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #angle2 = np.arccos(np.dot(v2, -v3) / (np.linalg.norm(v2) * np.linalg.norm(v3)))
        #angle3 = np.arccos(np.dot(v3, -v1) / (np.linalg.norm(v3) * np.linalg.norm(v1)))

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

def connect_to_grid(edge : HalfEdge) -> tuple[Face, Face]:
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

    if close_edge and far_edge:
        edge.next = close_edge
        close_edge.prev = edge

        edge.twin.prev = far_edge.twin
        far_edge.twin.next = edge.twin

    # Origin
    close_edge, far_edge = get_min_max_angle_edges(edge, edge.origin.edges)

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


def get_min_max_angle_edges(base_edge : HalfEdge, edge_list :list[HalfEdge]) -> tuple[HalfEdge, HalfEdge]:
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

    # TODO: durch angle-func ersetzen
    base_dir = base_edge.direction()
    base_dir = base_dir / np.linalg.norm(base_dir)  # Normalize

    if len(edge_list) == 0:
        return (None,None)

    angles = []
    for edge in edge_list:

        edge_dir = edge.direction()
        edge_dir = edge_dir / np.linalg.norm(edge_dir)  # Normalize

        # Calculate angle
        dot_product = np.dot(base_dir, edge_dir)
        cross_product = np.cross(base_dir, edge_dir)

        # Calculate angle in radians and make it oriented
        angle = np.degrees(np.arctan2(cross_product, dot_product))  # Arctan2 returns oriented angle

        # Cap angle in range 0 to 360
        angle = angle % 360
        angles.append((edge, angle))  # Convert angle to degrees

    # Find min and max angle
    min_edge, min_angle = min(angles, key=lambda x: x[1])
    max_edge, max_angle = max(angles, key=lambda x: x[1])

    return (min_edge, max_edge)