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

    tasks_to_do = [
        #"ortho_20_5a9e8244.instance.json",
        #"ortho_20_e2aff192.instance.json",
        #"point-set_10_4bcb7c21.instance.json",
        #"point-set_10_7451a2a9.instance.json",
        #"point-set_10_97578aae.instance.json",
        "point-set_10_13860916.instance.json",
        #"point-set_10_ae0fff93.instance.json",
        "point-set_10_c04b0024.instance.json",
        #"point-set_10_d009159f.instance.json",
        "point-set_10_f999dc7f.instance.json",
        #"point-set_20_0c4009d9.instance.json",
        "point-set_20_34a047f7.instance.json",
        #"point-set_20_41c48315.instance.json",
        #"point-set_20_54ab0b47.instance.json",
        "point-set_20_72cd2066.instance.json",
        "point-set_20_5868538a.instance.json",
        "simple-polygon_10_272aa6ea.instance.json",
        "simple-polygon_10_297edd18.instance.json",
        "simple-polygon_10_f2c8d74a.instance.json",
        "simple-polygon_20_0dda68ed.instance.json",
        "simple-polygon_20_4bd3c2e5.instance.json",
        "simple-polygon_20_35585ee3.instance.json",
        "simple-polygon-exterior_10_8b098f5e.instance.json",
        "simple-polygon-exterior_10_310dc6c7.instance.json",
        "simple-polygon-exterior_10_40642b31.instance.json",
        "simple-polygon-exterior_10_74050e4d.instance.json",
        "simple-polygon-exterior_10_a5f0f2fc.instance.json",
        "simple-polygon-exterior_10_c5616894.instance.json",
        "simple-polygon-exterior_20_2a7302a0.instance.json",
        "simple-polygon-exterior_20_87cff693.instance.json",
        "simple-polygon-exterior_20_92dcd467.instance.json",
        "simple-polygon-exterior_20_7520a1da.instance.json",
        "simple-polygon-exterior_20_c820ed5d.instance.json",
        "simple-polygon-exterior_20_ff791267.instance.json",
        "simple-polygon-exterior-20_10_6fbd9669.instance.json",
        "simple-polygon-exterior-20_10_8c4306da.instance.json",
        "simple-polygon-exterior-20_10_46c44a43.instance.json",
        "simple-polygon-exterior-20_10_868921c7.instance.json",
        "simple-polygon-exterior-20_10_15783346.instance.json",
        "simple-polygon-exterior-20_10_c6728228.instance.json",
        "simple-polygon-exterior-20_10_ce9152de.instance.json",
    ]

    for i in range(4,len(tasks_to_do)):
        #file = inp.get_random_file_from_dir()
        problem = inp.load_problem(tasks_to_do[i], folder)
        #vis.show_problem(problem)
        try: 
            solution = alg.non_obtuse_triangulation(problem)
            #vis.show_problem(problem)

            # visualize the solution
            #vis.show_result(problem, solution, show_faces=True)
            
            # visualize the problem and animate the solution steps
            #vis.animate_algorithm(problem, solution, interval=500, show_faces=True)

            if folder == "assets/final_tasks/":
                solution.convert_data()
                inp.save_result(solution, "assets/final_results/")
                #vis.show_results_by_final_data(solution)
            
            tasks_to_do.remove(tasks_to_do[i])
        except Exception as e:
            print(e)
            print(file)

            tb = e.__traceback__
            while tb:
                print(f"File: {tb.tb_frame.f_code.co_filename}, Line: {tb.tb_lineno}, Function: {tb.tb_frame.f_code.co_name}")
                tb = tb.tb_next
    
    print("End")
    print("Files to look at: ", tasks_to_do)
