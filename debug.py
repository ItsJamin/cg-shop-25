import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import numpy as np

if __name__ == '__main__':
    
    #problem = inp.load_problem("test.json")
    problem = inp.load_problem("debug2.json")
    #problem = inp.load_problem(inp.get_random_file_from_dir())
    
    # Problems that make problems:
    #problem = inp.load_problem("cgshop2025_examples_ortho_150_a39ede60.instance.json") #triangulation problem
    #problem = inp.load_problem("cgshop2025_examples_ortho_60_f31194db.instance.json") #triangulation problem
    problem = inp.load_problem("cgshop2025_examples_point-set_10_b4ff36df.instance.json") #steiner point recursion infinite problem
    

    solution = alg.non_obtuse_triangulation(problem)
    
    # visualize the problem and animate the solution steps. 
    vis.animate_algorithm(problem, solution, interval=100, show_faces=True)

    p1 = geo.Vertex(2,0)
    p2 = geo.Vertex(2,5)
    p3 = geo.Vertex(2,3)
    p4 = geo.Vertex(4,3)

    e1 = geo.HalfEdge(p1,p2)
    e2 = geo.HalfEdge(p3,p4)

    #print(geo.edges_intersect(e1, e2))

    pass