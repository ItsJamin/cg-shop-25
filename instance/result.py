import geometry as geo
import numpy as np

class Result():
    def __init__(self) -> None:

        #TODO: implement for result necessary variables (and funcs)
        
        self.v_elements = [] # list of elements to animate



    def step(self, object, color="orange"):
        """
        This function registers an object to be animated.

        object: Vertex, HalfEdge or Face
        """
        points = None
        if type(object) == geo.Vertex:
            points = object.position()
        elif type(object) == geo.HalfEdge and object.has_twin():
            points = np.concatenate([object.origin.position(),object.twin.origin.position()])
        elif type(object) == geo.Face:
            #print("Baue Animation")
            face_points = [v.position() for v in object.vertices]

            points = np.concatenate(face_points)
        else:
            raise Exception("Non-Animatible Object. Only Vertex or HalfEdge with twin")
    
        self.v_elements.append((points, color))