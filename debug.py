import visualization as vis
import inpout as inp
import geometry as geo

if __name__ == '__main__':
    

    problem = inp.load_problem("cgshop2025_examples_simple-polygon-exterior_10_34daa0f6.instance.json")

    print(problem.region_boundary)
    problem.create_geometry()
    c = problem.g_region_boundary
    d = c.twin
    for _ in range(len(problem.region_boundary)+1):
        if c.next is not None:
            print(f"{c.origin} {d.origin}")

            c = c.next
            d = d.next
        else:
            print(f"ERROR {c.next, d.next}")

    #vis.plot_problem(problem)

