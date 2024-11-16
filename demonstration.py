import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':
    problem = inp.load_problem("cgshop2025_examples_simple-polygon-exterior-20_80_23272e96.instance.json")
    
    # Führe den Greedy-Algorithmus aus
    alg.greedy_triangulation(problem)
    
    # Animation starten
    vis.animate_algorithm(problem, interval=500)