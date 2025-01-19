import json
import os

from instance import Problem
from instance import Result

def load_problem(filename : str, directory = "assets/") -> Problem:
    """Create instance of the problem."""
    with open(directory+filename, 'r') as f:
        data =json.load(f)
    
    problem_instance = Problem(data)
        
    return problem_instance

def save_result(result : Result, directory = "assets/final_results/"):

    data = {
        "content_type": "CG_SHOP_2025_Solution",
        "instance_uid": result.problem.instance_uid,
        "steiner_points_x": result.steiner_points_x,
        "steiner_points_y": result.steiner_points_y,
        "edges": result.edges
    }


    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = os.path.join(directory, f"{result.problem.instance_uid}.solution.json")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Result wurde erfolgreich gespeichert in: {filename}")
    except Exception as e:
        print(f"Fehler beim Speichern des Results {result.problem.instance_uid}: {e}")

    pass