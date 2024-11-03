import visualization as vis
import inpout as inp
import geometry as geo

if __name__ == '__main__':
    
    # So kann man testen

    v1 = geo.Vertex(4,5,None)
    v2 = geo.Vertex(9,23,None)
    e1 = geo.HalfEdge(v1, None)
    e2 = geo.HalfEdge(v2, e1)

    print(v1)
    print("Länge von Edge1", e1.length())

    # So auch

    problem = inp.load_problem("test.json")

    vis.plot_problem(problem)