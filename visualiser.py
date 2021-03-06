#########################################
#      Algorytmy Grafowe 2019/2020      #
#      Wizualizator w matplotlib        #
#          Krzysztof Podsiadlo          #
# https://github.com/Podsiadlo/GoGUI2/  #
#########################################


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
from matplotlib.widgets import Button
import json as js


class _Button_callback(object):
    def __init__(self, scenes):
        self.i = 0
        self.scenes = scenes

    def set_axis(self, ax):
        self.ax = ax

    def next(self, event):
        self.i = (self.i + 1) % len(self.scenes)
        self.draw()

    def prev(self, event):
        self.i = (self.i - 1) % len(self.scenes)
        self.draw()

    def draw(self):
        self.ax.clear()
        for collection in self.scenes[self.i].points:
            if len(collection.points) > 0:
                self.ax.scatter(*zip(*(np.array(collection.points))), c=collection.color, marker=collection.marker)
        for collection in self.scenes[self.i].lines:
            self.ax.add_collection(collection.get_collection())
        self.ax.autoscale()
        plt.draw()


class Scene:
    def __init__(self, points=[], lines=[]):
        self.points = points
        self.lines = lines


class PointsCollection:
    def __init__(self, points=[], color=None, marker=None):
        self.points = np.array(points)
        self.color = color
        self.marker = marker


class LinesCollection:
    def __init__(self, lines=[], color=None):
        self.color = color
        self.lines = lines[:]

    def add(self, line):
        self.lines.append(line)

    def get_collection(self):
        if self.color:
            return mcoll.LineCollection(self.lines, colors=mcolors.to_rgba(self.color))
        else:
            return mcoll.LineCollection(self.lines)


class Plot:
    def __init__(self, scenes=[], json=None):
        if json is None:
            self.scenes = scenes
        else:
            self.scenes = [Scene([PointsCollection(pointsCol) for pointsCol in scene["points"]],
                                 [LinesCollection(linesCol) for linesCol in scene["lines"]])
                           for scene in js.loads(json)]

    def __configure_buttons(self, callback):
        plt.subplots_adjust(bottom=0.2)
        axprev = plt.axes([0.6, 0.05, 0.15, 0.075])
        axnext = plt.axes([0.76, 0.05, 0.15, 0.075])
        bnext = Button(axnext, 'Następny')
        bnext.on_clicked(callback.next)
        bprev = Button(axprev, 'Poprzedni')
        bprev.on_clicked(callback.prev)
        return [bprev, bnext]

    def draw(self):
        plt.close()
        callback = _Button_callback(self.scenes)
        self.widgets = self.__configure_buttons(callback)
        callback.set_axis(plt.axes())
        # plt.show()
        callback.draw()

    def toJSON(self):
        return js.dumps([{"points": [pointCol.points.tolist() for pointCol in scene.points],
                          "lines": [linesCol.lines for linesCol in scene.lines]}
                         for scene in self.scenes])


if __name__ == '__main__':
    scenes = [Scene([PointsCollection([(1, 2), (3, 1.5), (2, -1)]),
                     PointsCollection([(5, -2), (2, 2), (-2, -1)], 'green', marker="^")],
                    [LinesCollection([[(1, 2), (2, 3)], [(0, 1), (1, 0)]], 'orange')]),
              Scene([PointsCollection([(1, 2), (-15, 1.5), (2, -1)], 'red'),
                     PointsCollection([(5, -2), (2, 2), (-2, 1)], 'black')],
                    [LinesCollection([[(-1, 2), (-2, 3)], [(0, -1), (-1, 0)]])])]

    plot = Plot(scenes)
    plot.draw()


#########################################
#      Algorytmy Grafowe 2019/2020      #
#        Wizualizator KD-drzewa         #
#          Stanislaw Denkowski          #
#          Maciej Tratnowiecki          #
#########################################


class KdtreeVisualiser:
    def __init__(self):
        self.points = []
        self.lines = []
        self.scenes = []
        self.rects = []
        self.res = []

    def put_points(self, points):
        self.points = points
        self.scenes.append(Scene([PointsCollection(self.points)]))

    def add_line(self, line, mark_points):
        self.lines.append(line)
        self.scenes.append(Scene([PointsCollection(self.points), PointsCollection(mark_points, 'orange')],
                                 [LinesCollection(self.lines)]
                                 ))

    def get_scenes(self):
        res = []
        res, self.scenes = self.scenes, res
        return res

    def add_search(self, scope, res=None):
        lowerleft, upperright = scope.get_tuple()
        upperleft = (lowerleft[0], upperright[1])
        lowerright = (upperright[0], lowerleft[1])
        self.rects += [[lowerleft,upperleft],[lowerright,upperright],[lowerleft,lowerright],[upperleft,upperright]]
        if res is not None:
            self.res += res
        self.scenes.append(Scene([PointsCollection(self.points), PointsCollection(self.res, 'red', marker='x')],
                                 [LinesCollection(self.rects), LinesCollection(self.rects[-4:],color='orange')]))
