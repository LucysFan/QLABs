import json
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import find_peaks
from utils.artist import Artist, CanvasWave
from utils.subtools import OpticWave
from scipy.fft import ifft


def plotter(rows, cols, 
            figsize, sharex, grids,
            waves, titles, colors, locations, xlabels, ylabels):
    
    fig, ax = plt.subplots(rows, cols, figsize = figsize, sharex = sharex)
    
    _c = 0
    for i in range(rows):
        for j in range(cols):
            w = waves[_c]
            t = titles[_c]
            c = colors[_c]
            g = grids[_c]
            l = locations[_c] 
            
            x = xlabels[_c]
            y = ylabels[_c]
            
            if cols > 1:
                ax[i, j].plot(w.x, w.y, label = w.label.lower(), color = c, linestyle = w.linestyle)
                ax[i, j].set_title(t)
                ax[i, j].legend(loc = l)
                ax[i, j].set_xlabel(x)
                ax[i, j].set_ylabel(y)
                ax[i, j].grid(g)
            else:
                ax[i].plot(w.x, w.y, label = w.label.lower(), color = c, linestyle = w.linestyle)
                ax[i].set_title(t)
                ax[i].legend(loc = l)   
                ax[i].set_xlabel(x)
                ax[i].set_ylabel(y)         
                ax[i].grid(g)    

            _c += 1
    
    plt.show()
    return 

def main(*args):
    
    waves = []
    for arg in args:
        _path, _headers = arg
        _wave = OpticWave(path = _path, headers = _headers)
        _wave.initialization()
        
        # _wave.time += 2 * np.max(_wave.time)
        
        hann = np.hanning(len(_wave.voltage))
        _wave.voltage *= hann
        

        ft = _wave.fft('voltage')         
        cw = CanvasWave(
            x         = np.linspace(0, 1, len(ft)),
            y         = ft,
            color     = 'random',
            label     = f'Signal_{args.index(arg)+1}',
            linestyle = '-' * (args.index(arg)+1))
        
        # dt = np.mean(np.diff(_wave.time)) / 4
        # df = 0.82e-14 / 4
        # df = 1 / 2.04885e-9
        sf = 2.5234937 * 3e8/1550e-9
        df = 1 / sf

        freq = _wave.fftfreq(len(ft), df)

        threshold = abs(freq[len(freq) // 2:-len(freq)//4:][np.argmax(np.abs(ft[len(ft) // 2: -len(ft)//4:]))])
        print(threshold/1e12)
        eps = 5e1

        ft[np.abs(freq) < threshold - eps] = 0
        ft[np.abs(freq) > threshold + eps] = 0

        reconstructed_signal = np.fft.ifft(ft)
        reconstructed_signal_real = np.real(reconstructed_signal)
        _wave.voltage = reconstructed_signal_real

        cwf = CanvasWave(
            x         = freq[len(freq) // 2:],
            y         = np.abs(ft)[len(ft) // 2:],
            color     = 'random',
            label     = f'Signal_{args.index(arg)+1}',
            linestyle = 'solid')
        
        f = threshold

        I = _wave.voltage * np.cos(2 * np.pi * f * _wave.time)
        Q = _wave.voltage * np.sin(2 * np.pi * f * _wave.time)
        phi = np.unwrap(np.arctan2(Q, I))
        phase = CanvasWave(
            x         = _wave.time,
            y         = phi,
            color     = 'random',
            label     = f'Signal_{args.index(arg)+1}',
            linestyle = 'solid')

        data = {
            'wave' : [_wave.time, _wave.voltage],
            'waveFFT' : cw,
            'waveFFTFREQ' : cwf,
            'phase' : phase
        }
        
        waves.append(data)
    
    # wavesVolt = [plt.plot(*w['wave']) for w in waves]
    # plt.show()
        
    wavesFFT = [w['waveFFT'] for w in waves]
    plotter(2, 1, figsize = (12, 12), sharex=True, grids = [True, True],
            waves = wavesFFT, titles = [r'$U(f_{indx})$', r'$U(f_{indx})$'],
            colors = ['green', 'orange'], locations = ['lower left', 'lower left'],
            xlabels = [None, None], ylabels = [None, None])
    
    wavesFFTFREQ = [w['waveFFTFREQ'] for w in waves]
    plotter(2, 1, figsize = (12, 12), sharex=True, grids = [True, True],
            waves = wavesFFTFREQ, titles = [r'$U(f)[V]$', r'$U(f)[V]$'],
            colors = ['green', 'orange'], locations = ['upper right', 'upper right'],
            xlabels = ['f[Hz]', 'f[Hz]'], ylabels = ['U(f)[V]', 'U(f)[V]'])
    
    wavesPHASE = [w['phase'] for w in waves]
    plotter(2, 1, figsize = (12, 12), sharex=True, grids = [True, True],
            waves = wavesPHASE, titles = [r'$\phi(t)$', r'$\phi(t)$'],
            colors = ['green', 'orange'], locations = ['upper right', 'upper right'],
            xlabels = ['f[Hz]', 'f[Hz]'], ylabels = [r'$\phi[rad]$', r'$\phi[rad]$'])    

    _df = wavesPHASE[0].y - wavesPHASE[1].y
    plt.plot(waves[0]['wave'][0], _df, color = 'blue')
    plt.ylabel(r'$\phi[rad]$')
    plt.xlabel('Time(s)')
    plt.title(r'$\delta\phi(t)$')
    plt.grid(True)
    plt.show()
    # plotter(2, 1, figsize = (12, 12), sharex=True, grids = [True, True],
    #         waves = wavesPHASE, titles = [r'$\phi(t)$', r'$\phi(t)$'],
    #         colors = ['red', 'yellow'], locations = ['upper right', 'upper right'],
    #         xlabels = ['Time(s)', 'Time(s)'], ylabels = [None, None])
    
    # _whs = [wh.y for wh in wavesPHASE]    

if __name__ == "__main__":
    path = 'utils/data/data.csv'
    h1 = ['Time(s)', 'CH1(V)']
    h2 = ['Time(s)', 'CH2(V)']
    main([path, h1], [path, h2])