import visualization as vis
import inpout as inp
import geometry as geo

if __name__ == '__main__':
    

    problem = inp.load_problem("cgshop2025_examples_simple-polygon-exterior_10_34daa0f6.instance.json")

    
    # Die Geometrischen Darstellungen des Problems befinden sich in diesen Variablen
    points = problem.g_points
    boundaries = problem.g_region_boundary
    constraints = problem.g_constraints 

    
    p1 = geo.Vertex(7000,500)
    p2 = geo.Vertex(1000,200)

    e1 = geo.create_full_edge(p1,p2)
    e2 = geo.create_full_edge(points[0], points[3])

    # Füge schrittweise Objekte hinzu, um sie nacheinander zu animieren
    problem.step(p1)
    problem.step(p2)
    problem.step(e1, "green")
    problem.step(e2)

    vis.animate_algorithm(problem, interval = 500)
