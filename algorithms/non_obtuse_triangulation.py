from instance import Problem, Result
import geometry as geo
import numpy as np
from .steiner_points import *
from .triangulation_greedy import *
from .triangulation_grid import *

def non_obtuse_triangulation(problem: Problem) -> Result:
    """
    Computes a top-down triangulation and fixes obtuse angles by placing Steiner points.
    """
    result = Result(problem=problem)

    #Grid-Triangulation
    #result = triangulation_grid(problem,result) (Lost Technology)
    
    #Greedy-Triangulation
    faces_to_look_at, all_edges, result = triangulation_greedy(problem, result)
    vis.show_result(problem, result)

    #Steiner Points
    result = steiner_points(faces_to_look_at, all_edges, problem, result)

    #TODO: Bombaclat

    return result

### Helper Functions