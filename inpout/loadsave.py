import json

from instance import Problem

def load_problem(filename : str) -> Problem:
    """Create instance of the problem."""
    with open("assets/"+filename, 'r') as f:
        data =json.load(f)
    
    problem_instance = Problem(data)
        
    return problem_instance

def save_result(result):
    # TODO: create result fiel from result object
    pass