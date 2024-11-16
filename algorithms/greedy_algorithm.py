from instance import Problem, Result
import geometry as geo

def greedy_triangulation(problem : Problem) -> Result:
    
    boundary_points = [problem.g_points[idx] for idx in problem.region_boundary]
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
                if geo.is_valid_triangle(edge1, edge2, edge3, edges):
                    if not geo.is_non_obtuse_triangle(edge1):
                        # If the triangle is obtuse, add a Steiner point on the longest edge
                        longest_edge = max([edge1, edge2, edge3], key=lambda e: e.length())
                        steiner_point = geo.add_steiner_point(longest_edge, problem.g_points)
                        problem.step(steiner_point, color="orange")
                        boundary_points.append(steiner_point)  # Add Steiner point to points list for future triangles
                        print(f"Steiner point added at {steiner_point}")

                    # Connect edges to form the triangle
                    geo.connect_edges(edge1, edge2)
                    geo.connect_edges(edge2, edge3)
                    geo.connect_edges(edge3, edge1)

                    # Add the edges to the list for intersection checking
                    edges.extend([edge1, edge2, edge3])

                    # Add triangle edges to animation steps
                    problem.step(edge1, color="blue")
                    problem.step(edge2, color="blue")
                    problem.step(edge3, color="blue")

                    # Debugging: Show triangle creation
                    print(f"Triangle created with vertices {v0}, {v1}, and {v2}")