import sys
import os

# HAUPTVERZEICHNIS IST BEI JEDEM ANDERS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r"C:\Users\Yunus\Documents\GitHub\SWP Anwendungen von Algos\cg-shop-25")))

from inpout.loadsave import load_problem
from instance import plot_instance
import matplotlib.pyplot as plt


problem_instance = load_problem("test.json")


fig, ax = plt.subplots()
plot_instance(ax, problem_instance)
plt.show()
