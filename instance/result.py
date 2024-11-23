import geometry as geo
import numpy as np

class Result():
    def __init__(self) -> None:

        #TODO: Implement for Result necessary variables (and funcs)
        
        self.v_elements = []



    def step(self, object, color="orange"):
        """
        Diese Funktion fügt ein Objekt zur Liste der zu animierenden Elemente hinzu.

        Parameter:
        - object (Vertex oder HalfEdge): Das zu animierende Objekt.
        - color (str, optional): Die Farbe des Objekts in der Animation. Standardmäßig "orange"
        """
        points = None
        if type(object) == geo.Vertex:
            points = object.position()
        elif type(object) == geo.HalfEdge and object.has_twin():
            points = np.concatenate([object.origin.position(),object.twin.origin.position()])
        elif type(object) == geo.Face:
            print("Baue Animation")
            face_points = [v.position() for v in object.get_vertices()]

            points = np.concatenate(face_points)
        else:
            raise Exception("Non-Animatible Object. Only Vertex or HalfEdge with twin")
    
        self.v_elements.append((points, color))