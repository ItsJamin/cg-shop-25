import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':
    
    problem = inp.load_problem("cgshop2025_examples_ortho_150_a39ede60.instance.json")

    solution = alg.greedy_top_down(problem)
    
    # visualize the problem and animate the solution steps. 
    vis.animate_algorithm(problem, solution, interval=10, show_faces=True)


    p1 = geo.Vertex(0,0)
    p2 = geo.Vertex(3,5)
    p3 = geo.Vertex(5,5)
    p4 = geo.Vertex(3,10)

    e1 = geo.HalfEdge(p1,p2, reference_from_below=True)

    fe2 = geo.HalfEdge(p2,p4)
    e2 = geo.HalfEdge(p2,p3)

    e3 = geo.HalfEdge(p3,p1)
    e4 = geo.HalfEdge(p4,p3)

    geo.connect_to_grid(fe2)
    geo.connect_to_grid(e2)
    geo.connect_to_grid(e3)
    geo.connect_to_grid(e4)

    pass