from instance import Problem, Result, convert_fraction_to_number
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from .colors import *

def plot_problem(instance: Problem):
    
    fig, ax = plt.subplots()

    ax.scatter(instance.points_x, instance.points_y, color="black")
    
    
    for i in range(len(instance.region_boundary)):
        x1, y1 = (
            instance.points_x[instance.region_boundary[i]],
            instance.points_y[instance.region_boundary[i]],
        )
        x2, y2 = (
            instance.points_x[
                instance.region_boundary[(i + 1) % len(instance.region_boundary)]
            ],
            instance.points_y[
                instance.region_boundary[(i + 1) % len(instance.region_boundary)]
            ],
        )
        ax.plot([x1, x2], [y1, y2], color="blue", linestyle="-")
    
    
    for constraint in instance.additional_constraints:
        x1, y1 = instance.points_x[constraint[0]], instance.points_y[constraint[0]]
        x2, y2 = instance.points_x[constraint[1]], instance.points_y[constraint[1]]
        ax.plot([x1, x2], [y1, y2], color="red", linestyle="-")
    
    ax.set_aspect("equal")
    ax.set_title(instance.instance_uid)

    return fig, ax


def animate_algorithm(instance: Problem, solution: Result, interval: int = 400, show_faces: bool = True):
    """
    Animate the algorithm steps in result.

    interval: time between animation steps (in milliseconds)
    show_faces: whether to show faces (default) in animation or not
    """

    # Nehme das visualisierte Problem als Vorlage
    fig, ax = plot_problem(instance)


    def update(data):

        points, color = data[0], data[1]

        # Punkt zeichnen
        if len(points) == 2:
            point = ax.scatter(points[0], points[1], color=color, zorder=5)

        # Linie zeichnen
        elif len(points) == 4:
            line = Line2D([points[0], points[2]], [points[1], points[3]], color=color)
            ax.add_line(line)

        # Polygon zeichnen
        elif len(points) > 4:
            polygon_points = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
            polygon = Polygon(polygon_points, closed=True, fill=True, facecolor=color, edgecolor="black", alpha=1, zorder=2)
            ax.add_patch(polygon)

    elems_to_animate = solution.v_elements

    # Zeige Faces nur wenn gewollt
    if not show_faces:
        elems_to_animate = [elem for elem in elems_to_animate if len(elem[0]) <= 4]

    # Animation erstellen
    ani = FuncAnimation(fig, update, frames=elems_to_animate, repeat=False, interval=interval)
    plt.show()


def show_result(instance: Problem, solution: Result, show_faces: bool = True):
    """
    Visualize the algorithm result all at once.

    show_faces: whether to show faces (default) in the visualization or not
    """

    # Nehme das visualisierte Problem als Vorlage
    fig, ax = plot_problem(instance)

    elems_to_draw = solution.v_elements

    # Zeige Faces nur wenn gewollt
    if not show_faces:
        elems_to_draw = [elem for elem in elems_to_draw if len(elem[0]) <= 4]

    for data in elems_to_draw:
        points, color = data[0], data[1]

        # Punkt zeichnen
        if len(points) == 2:
            ax.scatter(points[0], points[1], color=color, zorder=5)

        # Linie zeichnen
        elif len(points) == 4:
            line = Line2D([points[0], points[2]], [points[1], points[3]], color=color)
            ax.add_line(line)

        # Polygon zeichnen
        elif len(points) > 4:
            polygon_points = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
            polygon = Polygon(polygon_points, closed=True, fill=True, facecolor=color, edgecolor="black", alpha=1, zorder=2)
            ax.add_patch(polygon)

    # Zeige die finale Darstellung
    plt.show()


def show_problem(instance: Problem):
    """
    Visualize only the problem without any solution elements.
    """

    # Visualisiere nur das Problem
    fig, ax = plot_problem(instance)
    plt.show()

def show_results_by_final_data(result: Result):
    """
    Visualizes only the converted data of result
    """

    fig, ax = plt.subplots()

    points_x = result.points_x.copy()
    points_y = result.points_y.copy()
    
    ax.scatter(points_x, points_y, color="black")

    steiner_points_x = [convert_fraction_to_number(x) for x in result.steiner_points_x]
    steiner_points_y = [convert_fraction_to_number(y) for y in result.steiner_points_y]
    
    ax.scatter(steiner_points_x, steiner_points_y, color=CP_STEINER)

    points_x += steiner_points_x
    points_y += steiner_points_y

    for edge in result.edges:
        x1, y1 = points_x[edge[0]], points_y[edge[0]]
        x2, y2 = points_x[edge[1]], points_y[edge[1]]
        ax.plot([x1, x2], [y1, y2], color=CL_NORMAL, linestyle="-")
    
    ax.set_aspect("equal")
    #ax.set_title("Solution ", result.problem.instance_uid)

    plt.show()


