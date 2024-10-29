import json

# Erstelle eine Instanz vom Problem
def load_problem(filename):
    with open("assets/"+filename, 'r') as f:
        data =json.load(f)
    
    # TODO: Aus JSON ein Instanz-Objekt machen
    
        
    pass

def save_result(result):
    pass


load_problem("test.json")