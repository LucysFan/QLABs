from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


class Artist:
    
    def __init__(self, title : str,
                 figsize : list[int] = [12, 4],
                 dpi : int = 180,
                 fkwargs : dict = {},
                 akwargs : dict = {}):
        self.figsize = figsize
        self.title   = title
        self.dpi     = dpi
        self.__fkwargs = fkwargs # for future implementation
        self.__akwargs = akwargs

    
    def __create_canvas(self):
        self._fig = plt.figure(self.dpi, self.figsize)
        self._fig.suptitle(self.title)

        self._ax = plt.gca()
        self._ax.grid(True)
        
        return self._fig, self._ax
    
    def _plot(self, *args):
        for arg in args:
            self._ax.plot(arg.x, arg.y, color = arg.color, label = arg.label, linestyle = arg.linestyle)
        self._ax.legend(loc = 'upper left')
        return 0
        
    def __initialization(self, useLaTex, *args):
        self.__create_canvas()
        self._plot(*args)

        if useLaTex:
            plt.rcParams.update({
                "text.usetex": True,
                "font.family": "monospace",
                "font.monospace": 'Computer Modern Typewriter'
            })
        
        return 0
    
    def __update_frame(self, *args):
        for _ in range(10):
            for arg in args:
                arg.update()
        self._ax.clear()
        self._plot(*args)
        plt.pause(0.01)
        
        return 0
    
    def animate(self, *args, it = 10000, useLaTex = False, ):
        self.__initialization(useLaTex, *args)
        plt.ion()
        for _ in range(it):
            self.__update_frame(*args)  
        plt.ioff()    
        return 0
    
    def plot(self, *args, useLaTex = False):
        self.__initialization(useLaTex, *args)
        plt.show()
        return
        

@dataclass
class CanvasWave:
    x : np.ndarray
    y : np.ndarray
    color : str
    label : str
    linestyle : str
    
    def __post_init__(self):
        attrTypes = [np.ndarray, np.ndarray, str, str, str]
        attrs = {k : v for (k, v) in zip(self.__dict__.keys(), [(i, j) for (i,j) in zip(self.__dict__.values(), attrTypes)])}
        
        for (k,v) in attrs.items():
            vv  = v[0]
            w   = v[1]
            if not isinstance(vv, w):
                raise ValueError(f"'{k} = {vv}' should be {w} instead of {vv.__class__}")
