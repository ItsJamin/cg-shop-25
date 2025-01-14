import visualization as vis
import inpout as inp
import geometry as geo
import algorithms as alg
import numpy as np
import os
import math

if __name__ == '__main__':
    
    # Calculate Steiner Point
    """
    ((2595075828232919/549755813888, 6325546713094217/17592186044416)) -> ((1344388507559561/274877906944, 3122646701854677/8796093022208))
    ((1344388507559561/274877906944, 3122646701854677/8796093022208)) -> ((2688777015119711/549755813888, 6245293403708867/17592186044416))
    ((2688777015119711/549755813888, 6245293403708867/17592186044416)) -> ((2688777015119711/549755813888, 3122646701854425/8796093022208))
    ((2688777015119711/549755813888, 3122646701854425/8796093022208)) -> ((1344388507559561/274877906944, 3122646701854677/8796093022208))
    """

    p1 = geo.Vertex(667036,0)
    p2 = geo.Vertex(383537,0)
    p3 = geo.Vertex(1000000,422972)

    e1 = geo.HalfEdge(p1,p2)
    e2 = geo.HalfEdge(p2,p3)
    e3 = geo.HalfEdge(p3,p1)

    geo.connect_to_grid(e1)
    geo.connect_to_grid(e2)
    geo.connect_to_grid(e3)

    face = geo.Face(e1, reference_from_below=True)

    print(face._get_edges())

    steiner_point, changed_edge = alg.calculate_steiner_point(face)


    new_edge = geo.HalfEdge(steiner_point, p1)
    new_edge2 = geo.HalfEdge(steiner_point, p2)

    print(geo.angle_between_edges(new_edge2, new_edge))

    #print(alg.divide_steiner_point_quadrangle(e1.face))
    vis.plot_dcel([p1,p2,p3, steiner_point],[e1,e2,e3, new_edge])


    """

    pass

    origin = geo.Vertex(0,0)
    p1 = geo.Vertex(2595075828232919/549755813888, 6325546713094217/17592186044416)
    p2 = geo.Vertex(1344388507559561/274877906944, 3122646701854677/8796093022208)
    p3 = geo.Vertex(2688777015119711/549755813888, 6245293403708867/17592186044416)
    p4 = geo.Vertex(2688777015119711/549755813888, 3122646701854425/8796093022208)
    
    e1 = geo.HalfEdge(p1,p2)
    e2 = geo.HalfEdge(p2,p3)
    e3 = geo.HalfEdge(p3,p4)
    e4 = geo.HalfEdge(p4,p1)

    geo.connect_to_grid(e1)
    geo.connect_to_grid(e2)
    geo.connect_to_grid(e3)
    geo.connect_to_grid(e4)

    face = geo.Face(e1, reference_from_below=True)


    print(alg.divide_steiner_point_quadrangle(e1.face))
    vis.plot_dcel([origin,p1,p2,p3,p4],[e1,e2,e3,e4])

    pass
    """