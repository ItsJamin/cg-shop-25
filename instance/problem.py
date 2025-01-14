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
        self.g_constraints = []

        self.create_geometry()
    
    def create_geometry(self):

        self.g_points = []
        self.g_region_boundary = None
        self.g_constraints = []
        
        # create geoemtric points
        for x,y in zip(self.points_x,self.points_y):
            p = geo.Vertex(x,y)
            self.g_points.append(p)
        
        
        # closes bounding box with startpoint
        bound = self.region_boundary + [self.region_boundary[0]]
        last_edge = None
        start_edge = None

        # representing boundary by connected list of HalfEdges
        for i in range(len(bound)-1):
            print("GPOINT", self.g_points[bound[i]])
            current = geo.HalfEdge(self.g_points[bound[i]], self.g_points[bound[i+1]], reference_from_below=True, is_constraint=True)

            if last_edge is None:
                start_edge = current
            else:
                geo.connect_edges(last_edge, current)
            
            #geo.connect_to_grid(current)
            #current.origin.edges.append(current)
            #current.twin.origin.edges.append(current.twin)
            
            last_edge = current
        
        geo.connect_edges(last_edge, start_edge)
        #geo.connect_to_grid(current)

        self.g_region_boundary = geo.Face(start_edge)
        if self.g_region_boundary.is_clockwise():
            self.g_region_boundary = geo.Face(start_edge.twin)

        # additional constaints as HalfEdges
        for constraint in self.additional_constraints:
            a, b = constraint
            edge1 = geo.HalfEdge(self.g_points[a], self.g_points[b], is_constraint=True)
            geo.connect_to_grid(edge1)
            self.g_constraints.append(edge1)
        
        for p in self.g_points:
            print(p, p.edges)

    def validate_problem(self):
        # TODO: validate that the problem is well-formed
        pass

    