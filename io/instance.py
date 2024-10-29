class Problem():

    def __init__(self, 
                 instance_uid, 
                 num_points, 
                 points_x, 
                 points_y, 
                 region_boundary, 
                 num_constraints, 
                 additional_constraints):
        
        self.instance_uid = instance_uid
        self.num_points = num_points
        self.points_x = points_x
        self.points_y = points_y
        self.region_boundary = region_boundary
        self.additional_constraints = additional_constraints
        self.num_constraints = num_constraints
    
    
