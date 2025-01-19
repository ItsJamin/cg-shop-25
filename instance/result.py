import geometry as geo
import numpy as np

from .problem import Problem

class Result():
    def __init__(self, problem : Problem) -> None:

        #TODO: implement for result necessary variables (and funcs)

        self.problem = problem
        self.points_x = problem.points_x.copy()
        self.points_y = problem.points_y.copy()
        self.steiner_points_x = []
        self.steiner_points_y = []
        self.edges = convert_boundary_to_edge_list(self.problem.region_boundary) + self.problem.additional_constraints.copy()

        self.g_edges = []
        self.g_steiner_points = []

        self.v_elements = [] # list of elements to animate
    
    def convert_data(self):

        # Steiner points in fractions umwandeln und in x,y liste speichern
        for point in self.g_steiner_points:
            point_x = convert_float(point.x)
            point_y = convert_float(point.y)

            self.steiner_points_x.append(point_x)
            self.steiner_points_y.append(point_y)

        # Kantenpunktindizes suchen und in edges liste speichern.
        for edge in self.g_edges:
            origin = self._get_index_of_point(edge.origin)
            twin_origin = self._get_index_of_point(edge.twin.origin)

            self.edges.append([origin, twin_origin])
        
        
        print("--- Vollständige Repräsentation des Problems ---")
        print(" - Alle normalen Punkte: ", *zip(self.points_x, self.points_y))
        print(" - Alle Steinerpunkte: ", *zip(self.steiner_points_x, self.steiner_points_y))
        print(" - Alle Edges: ", self.edges)

    def _get_index_of_point(self, point : geo.Vertex):
        point_x = convert_float(point.x)
        point_y = convert_float(point.y)

        i = 0
        for x,y in zip(self.points_x + self.steiner_points_x, self.points_y + self.steiner_points_y):
            if x == point_x and y == point_y:
                return i
            i += 1
        
        raise Exception("Point not in list: ", point_x, point_y, "\n", self.problem.points_x)


    def step(self, object, color="orange"):
        """
        This function registers an object to be animated.

        object: Vertex, HalfEdge or Face
        """
        points = None
        if type(object) == geo.Vertex:
            points = object.position()
        elif type(object) == geo.HalfEdge and object.has_twin():
            points = np.concatenate([object.origin.position(),object.twin.origin.position()])
        elif type(object) == geo.Face:
            face_points = [v.position() for v in object._get_vertices()]

            points = np.concatenate(face_points)
        else:
            raise Exception("Non-Animatible Object. Only Vertex or HalfEdge with twin")
    
        self.v_elements.append((points, color))


def convert_float(value):
    # Versuche zu prüfen, ob es sich um einen Integer handelt
    print(value, type(value))
    if type(value) == int:
        return int(value)  # Gibt den Wert als Integer zurück
    elif type(geo.Fraction):
        if value.denominator == 1:
            return int(value.numerator)
        else:
            return str(value)
    else:
        # Konvertiere den Float in eine Fraction
        fraction = geo.create_fraction(value).limit_denominator()
        return str(fraction)
    
def convert_boundary_to_edge_list(boundary):
    return [[boundary[i-1], boundary[i]] for i in range(len(boundary))]

def convert_fraction_to_number(fraction_str):
    try:
        # Konvertiere den String in eine Fraction
        fraction = geo.create_fraction(fraction_str)
        
        # Überprüfe, ob der Wert eine ganze Zahl ist
        if fraction.denominator == 1:
            return int(fraction)  # Gibt die ganze Zahl als Integer zurück
        else:
            return float(fraction)  # Gibt die Bruchdarstellung als Float zurück
    except ValueError:
        raise ValueError("Ungültiges Format: Die Eingabe muss eine Fraktion wie 'a/b' sein.")
