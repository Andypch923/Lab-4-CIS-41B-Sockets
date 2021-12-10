import matplotlib.pyplot as plt
import numpy as np

class Graph:
    def xyPlot(self,xpoints,ypoints):
        plt.plot(xpoints,ypoints)
        plt.show()