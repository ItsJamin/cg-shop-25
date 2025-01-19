from geometry import Vertex, HalfEdge, Face, connect_to_grid
import geometry as geo
from algorithms import calculate_steiner_point, find_orthogonal_point

def test_calculate_steiner_point():
    """
    Teste ob calculate_steiner_point in einem gegeben, clockwise orientiertem, stumpfwinkligen Dreieck
    den richtigen Steinerpunkt (orthogonaler Schnittpunkt zum Stumpfen Winkel), berechnen kann.
    """

    # Hilfsfunktion: Erstelle ein stumpfwinkliges Dreieck
    def create_triangle(v1, v2, v3):
        vertex1 = Vertex(*v1)
        vertex2 = Vertex(*v2)
        vertex3 = Vertex(*v3)
        
        # Erstelle die HalfEdges
        edge1 = HalfEdge(vertex1, vertex2)
        edge2 = HalfEdge(vertex2, vertex3)
        edge3 = HalfEdge(vertex3, vertex1)

        connect_to_grid(edge1)
        connect_to_grid(edge2)
        connect_to_grid(edge3)

        # Erstelle die Face
        face = Face(edge1)
        if face.is_clockwise():
            return face
        return Face(edge1.twin)

    def test_case(A,B,C, expected_steiner_point):
        face = create_triangle(A, B, C)
        steiner_point, opposite_edge = calculate_steiner_point(face) #find_orthogonal_point(A,B,C)
        steiner_point = (geo.create_fraction(steiner_point.x), geo.create_fraction(steiner_point.y))

        assert steiner_point == expected_steiner_point, \
            f"Bei Punkte {A}, {B}, {C} ist {expected_steiner_point} erwartet und {steiner_point} Ergebnis der Funktion."

    test_case((13,3), (14,0), (0,0), (geo.create_fraction(13,1), geo.create_fraction(0,1)))
    test_case((5,2), (0,0), (10,0), (geo.create_fraction(5,1), geo.create_fraction(0,1)))
    test_case((3,3), (4,5), (1,1), (geo.create_fraction("2.68"), geo.create_fraction("3.24")))