
Our entry to the [CG:SHOP 2025](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2025/#problem-description) Competition.

# About the task

In the Planar Straight Line Graphs (PSLGs) variant of the Minimum Non-Obtuse Triangulation problem, the objective is to triangulate the area of a given PSLG 
G
, which is defined by a set of vertices and edges laid out in a plane such that the edges do not cross except at their endpoints. The triangulation must incorporate the existing edges of 
G
 and can include the addition of Steiner points anywhere in the plane, including on these edges. The placement of Steiner points is particularly challenging because it can affect the geometric properties of adjacent faces, thus complicating the triangulation process. All triangles formed in the solution must be non-obtuse, with each angle not exceeding 90 degrees, and the solution seeks to minimize the total number of Steiner points. This problem is complex due to its geometric constraints and the interdependencies introduced by Steiner points, making it a computationally demanding task likely belonging to the NP-hard class of problems. For a polygon, an example of a Minimum Non-Obtuse Triangulation can look like this:

![Example for a given problem (black) and possible solution (orange)](https://github.com/user-attachments/assets/2640fd49-93e2-410c-be28-7d688b3847f6)



# Our solution

Using a DCEL structure for the geometric representation we experimented with different approaches and techniques to solve this problem.

Our final process looks roughly like this:
![Second Example](https://github.com/user-attachments/assets/83917350-a56a-4129-99dd-16c4d7cdfa5b)


1. Top-Down Greedy-Triangulation

Triangulate the given polygon.

2. Steiner-Point-Triangulation

Take an obtuse triangulation and divide it using an orthogonal from the opposite edge of the obtuse angle to the obtuse angle.

3. Other techniques:

- Divide 4-Quadrangle (created through steiner points on the opposite triangle) into triangles
- Swap Edges (Try swapping the edge of two triangles to create two triangles which are not obtuse)
