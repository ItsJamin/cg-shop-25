import geometry as geo
import numpy as np

class Problem():

    def __init__(self, data):
        self.instance_uid = data["instance_uid"]
        self.num_points = data["num_points"]
        self.points_x = data["points_x"]
        self.points_y = data["points_y"]
        self.region_boundary = data["region_boundary"]
        self.additional_constraints = data["additional_constraints"]
        self.num_constraints = data["num_constraints"]

        self.g_points = []
        self.g_region_boundary = None
        self.g_constraints = []

        self.v_elements = [] # Liste der zu animierenden Elemente

        self.create_geometry()
    
    def create_geometry(self):

        self.g_points = []
        self.g_region_boundary = None
        self.g_constraints = []
        
        # Erstellen der Punkte
        for x,y in zip(self.points_x,self.points_y):
            p = geo.Vertex(x,y)
            self.g_points.append(p)
        
        
        # Schliesst Boundary-Kreis mit Startpunkt
        bound = self.region_boundary + [self.region_boundary[0]]
        last_edge = None

        # Boundary als HalfEdge-Verkettung realisieren
        for i in range(len(bound)-1):

            current = geo.create_full_edge(self.g_points[bound[i]], self.g_points[bound[i+1]])

            if last_edge is not None:
                geo.connect_edges(last_edge, current)
            else:
                self.g_region_boundary = current
            
            last_edge = current
        
        geo.connect_edges(last_edge, self.g_region_boundary)

        # Additional-Constraints als HalfEdge-Verkettung realisieren
        for constraint in self.additional_constraints:
            a, b = constraint
            edge1 = geo.create_full_edge(self.g_points[a], self.g_points[b])
            edge2 = edge1.twin
            self.g_constraints.append(edge1)

    def validate_problem(self):
        # TODO: Validiere dass das Problem korrekt formuliert ist
        pass

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
        else:
            raise Exception("Non-Animatible Object. Only Vertex or HalfEdge with twin")
    
        self.v_elements.append((points, color))
    
    def greedy_triangulation(self):
       
        boundary_points = [self.g_points[idx] for idx in self.region_boundary]
        num_points = len(boundary_points)
        edges = []  # Store all edges of triangles to check for intersections

        # Start triangulating by iterating through boundary points
        for i in range(num_points - 2):
            for j in range(i + 1, num_points - 1):
                for k in range(j + 1, num_points):
                    v0 = boundary_points[i]
                    v1 = boundary_points[j]
                    v2 = boundary_points[k]

                    # Create the triangle edges
                    edge1 = geo.create_full_edge(v0, v1)
                    edge2 = geo.create_full_edge(v1, v2)
                    edge3 = geo.create_full_edge(v2, v0)

                    # Check if the triangle is valid
                    if self.is_valid_triangle(edge1, edge2, edge3, edges):
                        if not self.is_non_obtuse_triangle(edge1):
                            # If the triangle is obtuse, add a Steiner point on the longest edge
                            longest_edge = max([edge1, edge2, edge3], key=lambda e: e.length())
                            steiner_point = self.add_steiner_point(longest_edge)
                            boundary_points.append(steiner_point)  # Add Steiner point to points list for future triangles
                            print(f"Steiner point added at {steiner_point}")

                        # Connect edges to form the triangle
                        geo.connect_edges(edge1, edge2)
                        geo.connect_edges(edge2, edge3)
                        geo.connect_edges(edge3, edge1)

                        # Add the edges to the list for intersection checking
                        edges.extend([edge1, edge2, edge3])

                        # Add triangle edges to animation steps
                        self.step(edge1, color="blue")
                        self.step(edge2, color="blue")
                        self.step(edge3, color="blue")

                        # Debugging: Show triangle creation
                        print(f"Triangle created with vertices {v0}, {v1}, and {v2}")

    def edges_intersect(edge1, edge2):
        
        
        def ccw(A, B, C):
            # Returns True if the points A, B, and C are in counterclockwise order
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        # Extract vertices of both edges
        A, B = edge1.origin, edge1.twin.origin
        C, D = edge2.origin, edge2.twin.origin

        # Check if the line segments AB and CD intersect
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    
    def is_valid_triangle(self, edge1, edge2, edge3, existing_edges):
       
        for existing_edge in existing_edges:
            if (Problem.edges_intersect(edge1, existing_edge) or 
                Problem.edges_intersect(edge2, existing_edge) or 
                Problem.edges_intersect(edge3, existing_edge)):
                return False
        
        # Optionally, check if the triangle is within the boundary if needed
        # Example: Use a point-in-polygon test for one vertex or center of triangle
        
        return True


    
    def is_non_obtuse_triangle(self, edge):
        # Prüft, ob edge und seine Nachbarn existieren und alle Twin-Edges haben
        if edge.has_twin() and edge.next and edge.next.has_twin():
            # Berechne die Richtungsvektoren der Kanten des Dreiecks
            v1 = edge.direction()
            v2 = edge.next.direction()
            v3 = edge.next.next.direction()

            # Berechne die Winkel zwischen den Kantenpaaren
            angle1 = np.arccos(np.dot(v1, -v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            angle2 = np.arccos(np.dot(v2, -v3) / (np.linalg.norm(v2) * np.linalg.norm(v3)))
            angle3 = np.arccos(np.dot(v3, -v1) / (np.linalg.norm(v3) * np.linalg.norm(v1)))
            
            # Prüfe, ob alle Winkel ≤ 90 Grad sind (π/2)
            return all(angle <= np.pi / 2 for angle in [angle1, angle2, angle3])
        
        return False  # Falls kein gültiges Dreieck vorliegt

    def add_steiner_point(self, edge):
     
        # Setze den Punkt auf die Winkelhalbierende des stumpfen Winkels
        midpoint_x = (edge.origin.x + edge.twin.origin.x) / 2
        midpoint_y = (edge.origin.y + edge.twin.origin.y) / 2
        steiner_point = geo.Vertex(midpoint_x, midpoint_y)
        
        self.g_points.append(steiner_point)
        return steiner_point

