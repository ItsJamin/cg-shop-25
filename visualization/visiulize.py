import sys
import os


from .inpout import instance as i
import matplotlib.pyplot as plt


#problem_instance = n.load_problem("test.json")


fig, ax = plt.subplots()
plot_instance(ax, None)#problem_instance)
plt.show()
