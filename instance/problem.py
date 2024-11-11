import geometry as geo
import numpy as np

class Problem():

    def __init__(self, data):
        self.instance_uid = data["instance_uid"]
        self.num_points = data["num_points"]
        self.points_x = data["points_x"]
        self.points_y = data["points_y"]
        self.region_boundary = data["region_boundary"]
        self.additional_constraints = data["additional_constraints"]
        self.num_constraints = data["num_constraints"]

        self.g_points = []
        self.g_region_boundary = None
        self.g_constraints = []

        self.v_elements = [] # Liste der zu animierenden Elemente

        self.create_geometry()
    
    def create_geometry(self):

        self.g_points = []
        self.g_region_boundary = None
        self.g_constraints = []
        
        # Erstellen der Punkte
        for x,y in zip(self.points_x,self.points_y):
            p = geo.Vertex(x,y)
            self.g_points.append(p)
        
        
        # Schliesst Boundary-Kreis mit Startpunkt
        bound = self.region_boundary + [self.region_boundary[0]]
        last_edge = None

        # Boundary als HalfEdge-Verkettung realisieren
        for i in range(len(bound)-1):

            current = geo.create_full_edge(self.g_points[bound[i]], self.g_points[bound[i+1]])

            if last_edge is not None:
                geo.connect_edges(last_edge, current)
            else:
                self.g_region_boundary = current
            
            last_edge = current
        
        geo.connect_edges(last_edge, self.g_region_boundary)

        # Additional-Constraints als HalfEdge-Verkettung realisieren
        for constraint in self.additional_constraints:
            a, b = constraint
            edge1 = geo.create_full_edge(self.g_points[a], self.g_points[b])
            edge2 = edge1.twin
            self.g_constraints.append(edge1)

    def validate_problem(self):
        # TODO: Validiere dass das Problem korrekt formuliert ist
        pass

    def step(self, object, color="orange"):
        """
        Diese Funktion fügt ein Objekt zur Liste der zu animierenden Elemente hinzu.

        Parameter:
        - object (Vertex oder HalfEdge): Das zu animierende Objekt.
        - color (str, optional): Die Farbe des Objekts in der Animation. Standardmäßig "orange"
        """
        points = None
        if type(object) == geo.Vertex:
            points = object.position()
        elif type(object) == geo.HalfEdge and object.has_twin():
            points = np.concatenate([object.origin.position(),object.twin.origin.position()])
        else:
            raise Exception("Non-Animatible Object. Only Vertex or HalfEdge with twin")
    
        self.v_elements.append((points, color))

