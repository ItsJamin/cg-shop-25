from instance import Problem, Result
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

def animate_algorithm(instance: Problem, solution: Result, interval : int = 400):
    """
    Animiert die (Lösungs-)Schritte in einem Problem mit Warteintervallen in Millisekunden.
    """

    #TODO: add faces

    # Nehme das visualisierte Problem als Vorlage
    fig, ax = plot_problem(instance)

    def update(data):
        # Schrittweise Vertices oder Linien zeichnen
        points, color = data[0], data[1]
        if len(points) == 2:
            ax.scatter(points[0], points[1], color = color)
        elif len(points) == 4:
            ax.plot([points[0], points[2]], [points[1], points[3]], color=color, linestyle="-")

    # Animation erstellen
    ani = FuncAnimation(fig, update, frames=solution.v_elements, repeat=False, interval = interval)
    plt.show()