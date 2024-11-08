import geometry as geo

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
        self.g_num_constraints = None
    
    def create_geometry(self):

        self.g_points = []
        self.g_region_boundary = None
        self.g_num_constraints = None
        
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
        
        

    

    def validate_problem(self):
        # TODO: Validiere dass das Problem korrekt formuliert ist
        pass
    

