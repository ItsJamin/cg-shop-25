from instance import Problem, Result
import geometry as geo
import numpy as np
import visualization as vis

def triangulation_grid(problem, result):


    
    return(faces_to_look_at, all_edges, result)

# TODO:
# 1. punkte auf region boundary setzen: nicht mit rboundary berühren
    # 2. liste an punkte nur  auf boundary
    # 3. punkte von oben durch gehen


    
#Helper Functions

def sort_points_top_down(liste : list[geo.Vertex]) -> list[geo.Vertex]:
    """
    Sort list of points from top to bottom (y-axis)
    """

    n = len(liste)
    for i in range(n):
        for j in range(i + 1, n):
            if liste[i].y < liste[j].y:
                liste[i], liste[j] = liste[j], liste[i]
    return liste