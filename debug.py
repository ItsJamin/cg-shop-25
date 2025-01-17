import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import numpy as np
import os
import math

if __name__ == '__main__':

    """
    vis.debug_edges([
    ((1000000, 422972), (383537, 0)),
    ((383537, 0), (0, 0)),
    ((0, 0), (1000000, 422972)),
    ((1000000, 422972), (667036, 0)),
    ((667036, 0), (0, 0)),
    ((0, 0), (383537, 0)),
    ((383537, 0), (383537, -232707)),
    ((383537, -232707), (667036, -232707)),
    ((667036, -232707), (667036, 0)),
    ((667036, 0), (1000000, 0)),
    ((1000000, 0), (1000000, 422972)),
    ((1000000, 422972), (1000000, 834548)),
    ((1000000, 834548), (1000000, 1000000)),
    ((1000000, 1000000), (0, 1000000)),
    ((0, 1000000), (0, 0)),
    ((0, 0), (667036, 0)),
    ((667036, 0), (383537, 0))
]
, delay=3
    )
    """
    
    
    # Calculate Steiner Point
    """
    ((2595075828232919/549755813888, 6325546713094217/17592186044416)) -> ((1344388507559561/274877906944, 3122646701854677/8796093022208))
    ((1344388507559561/274877906944, 3122646701854677/8796093022208)) -> ((2688777015119711/549755813888, 6245293403708867/17592186044416))
    ((2688777015119711/549755813888, 6245293403708867/17592186044416)) -> ((2688777015119711/549755813888, 3122646701854425/8796093022208))
    ((2688777015119711/549755813888, 3122646701854425/8796093022208)) -> ((1344388507559561/274877906944, 3122646701854677/8796093022208))
    """

    result = inp.Result(problem=inp.load_problem("test.json"))

    p1 = geo.Vertex(0,0)
    p2 = geo.Vertex(10,0)
    p3 = geo.Vertex(-2,5)

    e1 = geo.HalfEdge(p1,p2)
    e2 = geo.HalfEdge(p2,p3)
    e3 = geo.HalfEdge(p3,p1)

    geo.connect_to_grid(e1)
    geo.connect_to_grid(e2)
    geo.connect_to_grid(e3)

    face = geo.Face(e1, reference_from_below=True)

    print("Anfängliche Verbindung")
    print(face._get_edges())

    steiner_point, changed_edge = alg.calculate_steiner_point(face)

    #faces = alg.add_steiner_point_to_triangulation(steiner_point, face, [], changed_edge, result)

    #new_edge = geo.HalfEdge(steiner_point, p1)
    #new_edge2 = geo.HalfEdge(steiner_point, p2)

    #print("Winkel zwischen ", geo.angle_between_edges(new_edge2, new_edge))

    #print(face._get_edges())
    #for f in faces:
    #    print("F", f._get_edges())

    #print(alg.divide_steiner_point_quadrangle(e1.face))
    vis.plot_dcel([p1,p2,p3, steiner_point],[e1,e2,e3])

    