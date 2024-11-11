import visualization as vis
import inpout as inp
import geometry as geo

if __name__ == '__main__':
    problem = inp.load_problem("test.json")
    
    # Führe den Greedy-Algorithmus aus
    problem.greedy_triangulation()
    
    # Animation starten
    vis.animate_algorithm(problem, interval=1000)