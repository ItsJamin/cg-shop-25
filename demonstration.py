import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':

    # ----- Main Logic ----- #

    # create problem from json file
    #problem = inp.load_problem("test.json")
    #problem = inp.load_problem("cgshop2025_examples_simple-polygon_10_81177380.instance.json")
    problem = inp.load_problem("cgshop2025_examples_simple-polygon-exterior-20_10_a557fecb.instance.json")
    #problem = inp.load_problem(inp.get_random_file_from_dir())
    #problem = inp.load_problem("cgshop2025_examples_ortho_60_f31194db.instance.json") 

    # execute the greedy algorithm
    solution = alg.non_obtuse_triangulation(problem)

    # save the solution
    #inp.save_result(solution, "test_solution")

    # visualize the problem
    #vis.show_problem(problem)

    # visualize the solution
    vis.show_result(problem, solution, show_faces=True)
    
    # visualize the problem and animate the solution steps
    vis.animate_algorithm(problem, solution, interval=300, show_faces=True)

    # ----- Geometric Representation ----- #

    print("\n---Geometric Representation---\n")

    p1 = geo.Vertex(0,0)
    p2 = geo.Vertex(5,0)
    p3 = geo.Vertex(0,5)

    # creates HalfEdge but also TwinHalfEdge and sets pointer properly
    e1 = geo.HalfEdge(p1, p2)
    e2 = geo.HalfEdge(p2, p3)
    e3 = geo.HalfEdge(p3, p1)

    # through this, edges will be connected and faces created properly
    geo.connect_to_grid(e1)
    geo.connect_to_grid(e2)
    geo.connect_to_grid(e3)

    face = e1.twin.face # geo.Face

    print(f"The face {face} is clockwise-oriented: {face.is_clockwise()}")

    print("Angle between on first point: ", geo.angle_between_edges(e1, e1.prev.twin))

