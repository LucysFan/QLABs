import functools

import numpy as np
import pandas as pd

class Time:
    def __get__(self, obj, objType = None):
        return obj._time
    
    def __set__(self, obj, value):
        if not isinstance(value, np.ndarray | pd.core.frame.DataFrame | pd.core.series.Series):
            raise ValueError("time can either be np.ndarray or it will be converted to np.ndarray from Series or one dimentional Data Frame")
        if not len(value.shape) == 1:
            raise ValueError("time can only be one dimentional")
        if not isinstance(value, np.ndarray):
            obj._time = value.to_numpy()
        else:
            obj._time = value    

class Voltage:
    def __get__(self, obj, objType = None):
        return obj._voltage
    
    def __set__(self, obj, value):
        if not isinstance(value, np.ndarray | pd.core.frame.DataFrame | pd.core.series.Series):
            raise ValueError("voltage can either be np.ndarray or it will be converted to np.ndarray from Series or one dimentional Data Frame")
        if not len(value.shape) == 1:
            raise ValueError("Voltage can only be one dimentional")
        if not isinstance(value, np.ndarray):
            obj._voltage = value.to_numpy()
            return
        obj._voltage = value    
        
class Signal:
    def __get__(self, obj, objType = None):
        return obj._signal
    def __set__(self, obj, value):
        if not isinstance(value, pd.core.frame.DataFrame):
            raise ValueError("signal can obly be signalData frame")
        if not (value.shape[-1] == 2 and len(value.shape) == 2):
            raise ValueError("Signal shape can only be two dimentional")
        obj._signal = value
        
def time(attr):
    def _wrapper(cls):
        setattr(cls, attr, Time())
        return cls
    return _wrapper

def voltage(attr):
    def _wrapper(cls):
        setattr(cls, attr, Voltage())
        return cls
    return _wrapper

def signal(attr):
    def _wrapper(cls):
        setattr(cls, attr, Signal())
        return cls
    return _wrapper

@time("time")
@voltage("voltage")
class WavePacket:
    def __init__(self, 
                 time    : np.ndarray | pd.core.frame.DataFrame, 
                 voltage : np.ndarray | pd.core.frame.DataFrame):

        self.voltage = voltage
        # self.signal  = signal
        self.time    = time
    
    @staticmethod
    def __import(_import_):
        def decorator(func):
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                if not isinstance(_import_, str):
                    raise ValueError("module name can only be string")
                module = __import__(_import_)
                return func(*args, module, **kwargs)
            return _wrapper
        return decorator
    
    @__import("scipy")
    def fft(self, arg : str, scipy, **kwargs):
        if not isinstance(arg, str):
            raise ValueError("argument must be a string")
        return scipy.fft.fft(getattr(self, arg), **kwargs)
    
    @__import("scipy")
    def rfft(self, arg : str, scipy):
        if not isinstance(arg, str):
            raise ValueError("argument must be a string")
        return scipy.fft.rfft(getattr(self, arg))
    
    @__import("scipy")
    def fftfreq(self, n, d, scipy):
        return scipy.fft.fftfreq(n, d)

    @__import("matplotlib")
    def plot(self, arg : str, matplotlib, **kwargs):
        if not isinstance(arg, str):
            raise ValueError("argument must be a string")
        matplotlib.pyplot.plot(getattr(self, arg), **kwargs)


class DataSignal:
    def __init__(self, path):
        self.path = path
        self.signalData = None
    
    def __get_signalData(self):
        return pd.read_csv(self.path)
    
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path : str):
        try:
            if self.__set_path:
                raise TypeError('cannot change constant value')
        except AttributeError:
            self._path = path
            self.__set_value = True

    @property
    def signalData(self):
        return self._signalData
    
    @signalData.setter
    def signalData(self, *args, **kwargs):
        try:
            if self.__set_signalData:
                raise TypeError("cannot change constant value")
        except AttributeError:
            self._signalData = self.__get_signalData()
            self.__set_signalData = True