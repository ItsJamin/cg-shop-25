import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import numpy as np
import os

if __name__ == '__main__':
    
    problem = inp.load_problem("test.json")
    #problem = inp.load_problem("debug2.json")
    #problem = inp.load_problem(inp.get_random_file_from_dir("assets/final_tasks"), "assets/final_tasks/")
    
    # Problems that make problems:
    #problem = inp.load_problem("cgshop2025_examples_ortho_150_a39ede60.instance.json") #triangulation problem
    #problem = inp.load_problem("cgshop2025_examples_ortho_60_f31194db.instance.json") #triangulation problem
    #problem = inp.load_problem("cgshop2025_examples_point-set_10_b4ff36df.instance.json") #steiner point recursion infinite problem
    for file in os.listdir("assets/final_tasks"):
        print("-----", file)
        try:
            problem = inp.load_problem(file, "assets/final_tasks/")

            solution = alg.non_obtuse_triangulation(problem)
            solution.convert_data()
            vis.show_results_by_final_data(solution)
            inp.save_result(solution)
        except:
            print(f"{file} poascht net")

    #print("################################")
    #print("Solution Points:", solution.g_steiner_points)
    #print("Solution Edges:", solution.g_edges)
    #vis.show_result(problem, solution, show_faces=True)

    pass