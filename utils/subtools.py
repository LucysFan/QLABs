import numpy as np
import traceback

from .opticSignal import WavePacket, DataSignal

class OpticWave(WavePacket, DataSignal):
    def __init__(self, 
                 time = np.array([]), voltage = np.array([]),
                 path = '', headers = []):
        
        if not all([time, voltage]):
            if path is None:
                raise AttributeError("either time, voltage, signal or path should be known")
            else:
                if not headers:
                    raise AttributeError("headers should be known if path is established")
                if not type(headers) == list:
                    raise ValueError("headrs should be a list")
                
                DataSignal.__init__(self, path)
                self.__path_init = True
        else:
            WavePacket.__init__(self, time, voltage)
            self.__path_init = False
        
        self.__initializationCompleted = False
        self.time = time
        self.voltage = voltage
        self.headers = headers
    
    def __initialization(self):
        if self.__path_init:
            data = self.signalData
            _th, _vh = self.headers
            WavePacket.__init__(self, time = data[_th],  voltage = data[_vh])
        return 
    
    def initialization(self):
        try:
            if self.__initializationCompleted:
                print("Assertion : initialization already has been completed")
            else:
                self._OpticWave__initialization()
                self.__initializationCompleted = True
        except Exception as e:
            print(f"exception {e.__class__} was caught, initialization aborted")
            traceback.print_exc()


# s = OpticWave(path = 'utils/data/signal.csv', headers = ['Time(s)', 'CH1(V)'])
# s.initialization()
# print(s.voltage)
# print(type(s.voltage))