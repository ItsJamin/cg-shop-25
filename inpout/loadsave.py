import json

from instance import Problem

# Erstelle eine Instanz vom Problem
def load_problem(filename):
    with open("assets/"+filename, 'r') as f:
        data =json.load(f)
    
    problem_instance = Problem(data)
        
    return problem_instance

def save_result(result):
    # TODO: aus Result Objekt eine Result Datei machen
    pass