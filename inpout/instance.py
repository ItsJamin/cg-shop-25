class Problem():

    def __init__(self, data):
        self.instance_uid = data["instance_uid"]
        self.num_points = data["num_points"]
        self.points_x = data["points_x"]
        self.points_y = data["points_y"]
        self.region_boundary = data["region_boundary"]
        self.additional_constraints = data["additional_constraints"]
        self.num_constraints = data["num_constraints"]
    

    def validate_problem(self):
        # TODO: Validiere dass das Problem korrekt formuliert ist
        pass
    

