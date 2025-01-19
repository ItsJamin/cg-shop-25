import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import traceback
import sys
import time

if __name__ == '__main__':

    # ----- Main Logic ----- #

    # create problem from json file
    #problem = inp.load_problem("test.json")

    # still making problems:
    # Face is not closed:
    # - cgshop2025_examples_simple-polygon-exterior-20_80_23272e96.instance.json
    # - cgshop2025_examples_point-set_250_c4545664.instance.json
    # - cgshop2025_examples_point-set_150_3334f8a1.instance.json
    # - cgshop2025_examples_simple-polygon-exterior-20_60_5da99fdb.instance.json
    # - cgshop2025_examples_simple-polygon_40_986defab.instance.json
    # - cgshop2025_examples_ortho_80_f9b89ad1.instance.json

    #sys.set_int_max_str_digits(99000)
    # Optimierungsmöglichkeiten
    # angle-between-edges möglichst wenig benutzt
    # -> durch effizientere funktion ersetzen
    # parallelisieren (?)

    print("Starting...")
    file = "ortho_10_d2723dcc.instance.json"
    folder = "assets/final_tasks/"

    for i in range(1):
        #file = inp.get_random_file_from_dir()
        problem = inp.load_problem(file, folder)
        #vis.show_problem(problem)
        try: 
            solution = alg.non_obtuse_triangulation(problem)
            #vis.show_problem(problem)

            # visualize the solution
            vis.show_result(problem, solution, show_faces=True)
            
            # visualize the problem and animate the solution steps
            vis.animate_algorithm(problem, solution, interval=500, show_faces=True)

            if folder == "assets/final_tasks/":
                solution.convert_data()
                inp.save_result(solution, "assets/final_results/")
                vis.show_results_by_final_data(solution)
        except Exception as e:
            print(e)
            print(file)

            tb = e.__traceback__
            while tb:
                print(f"File: {tb.tb_frame.f_code.co_filename}, Line: {tb.tb_lineno}, Function: {tb.tb_frame.f_code.co_name}")
                tb = tb.tb_next
    
    print("End")
