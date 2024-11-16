import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':
    problem = inp.load_problem("cgshop2025_examples_ortho_20_b099d1fe.instance.json")
    
    # Führe den Greedy-Algorithmus aus
    alg.greedy_top_down(problem)
    
    # Animation starten
    vis.animate_algorithm(problem, interval=800)