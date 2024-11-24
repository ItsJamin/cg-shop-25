import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':

    # create problem from json file
    problem = inp.load_problem("cgshop2025_examples_simple-polygon-exterior_20_98b56c77.instance.json")
    
    # execute the greedy algorithm
    solution = alg.greedy_top_down(problem)
    
    # visualize the problem and animate the solution steps. 
    vis.animate_algorithm(problem, solution, interval=800, show_faces=False)