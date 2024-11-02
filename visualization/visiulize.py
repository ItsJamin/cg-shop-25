import sys
import os

sys.path.append(os.getcwd())

from inpout import load_problem
from instance import plot_instance
import matplotlib.pyplot as plt


problem_instance = load_problem("test.json")


fig, ax = plt.subplots()
plot_instance(ax, problem_instance)
plt.show()
