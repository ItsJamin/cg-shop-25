import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import numpy as np

if __name__ == '__main__':
    
    problem = inp.load_problem("test.json")
    #problem = inp.load_problem("cgshop2025_examples_ortho_150_a39ede60.instance.json")
    #problem = inp.load_problem(inp.get_random_file_from_dir())

    solution = alg.greedy_top_down(problem)
    #solution.step(problem.g_region_boundary)
    
    # visualize the problem and animate the solution steps. 
    vis.animate_algorithm(problem, solution, interval=500, show_faces=True)

    p1 = geo.Vertex(2,0)
    p2 = geo.Vertex(2,5)
    p3 = geo.Vertex(2,3)
    p4 = geo.Vertex(4,3)

    e1 = geo.HalfEdge(p1,p2)
    e2 = geo.HalfEdge(p3,p4)

    #print(geo.edges_intersect(e1, e2))

    pass