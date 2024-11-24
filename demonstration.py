import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg

if __name__ == '__main__':

    # create problem from json file
    problem = inp.load_problem("test.json")
    #problem = inp.load_problem(inp.get_random_file_from_dir())

    # execute the greedy algorithm
    solution = alg.greedy_top_down(problem)
    
    # visualize the problem and animate the solution steps. 
    vis.animate_algorithm(problem, solution, interval=10, show_faces=True)