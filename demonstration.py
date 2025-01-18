import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import traceback

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

    print("Starting...")
    file = "cgshop2025_examples_simple-polygon_40_986defab.instance.json"#
    folder = "assets/"

    for i in range(1):
        #file = inp.get_random_file_from_dir()
        problem = inp.load_problem(file, folder)
        vis.show_problem(problem)
        try: 
            solution = alg.non_obtuse_triangulation(problem)
            #vis.show_problem(problem)

            # visualize the solution
            vis.show_result(problem, solution, show_faces=True)
            
            # visualize the problem and animate the solution steps
            vis.animate_algorithm(problem, solution, interval=500, show_faces=True)
        except Exception as e:
            print(e)
            print(file)

            tb = e.__traceback__
            while tb:
                print(f"File: {tb.tb_frame.f_code.co_filename}, Line: {tb.tb_lineno}, Function: {tb.tb_frame.f_code.co_name}")
                tb = tb.tb_next
    
    print("End")
