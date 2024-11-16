import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':

    # Erstelle das Problem aus der JSON-Datei
    problem = inp.load_problem("cgshop2025_examples_ortho_20_b099d1fe.instance.json")
    
    # Führe den Greedy-Algorithmus aus
    solution = alg.greedy_top_down(problem)
    
    # Visualisiere das Problem und animiere was der Algorithmus erstellt hat. 
    vis.animate_algorithm(problem, solution, interval=800)