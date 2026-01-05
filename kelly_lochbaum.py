# A simple Kelly & Lochbaum (1962) vocal-tract model for vowels.

# Derived, in part, from MATLAB code provided by Siddharth Mathur to supplement
# the following papers:
#
# Mathur, S. and Story, B., Vocal tract modeling: Implementation of continuous
# length variations in a half-sample delay Kelly-Lochbaum model, ISSPIT, 2003.
# https://ieeexplore.ieee.org/document/1341230
#
# Mathur S., Story B., and Rodriguez J., Vocal-Tract Modeling: Fractional
# Elongation of Segment Lengths in a Waveguide Model With Half-Sample Delays,
# IEEE Transaction on Audio Speech and Language Processing, 2006.
# https://ieeexplore.ieee.org/document/1677994
#
# in part, from MATLAB code provided by Jont B Allen to compute the response of
# a vowel for HW05 of ECE-537, dated 12 Sep 2004 and 16 Sep 2006, and, in part,
# from code written in MATLAB and Scheme by Anchal Dube.
#
# The code provided by Siddharth Mathur is (C) 2006 Siddharth Mathur.
# The code provided by Jont B Allen is copyright: Jont B Allen.

import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt

#\needswork
# AD to fit to spectrum of speech sample

def two_tube(A0, l0, A1, l1):
    return np.array([A0]*l0+[A1]*l1)

# 22-tube models. At the default parameters, simulates a vocal tract of length
# 17.46031746031746 cm.
A_a =  two_tube(1.0, 12, 7.0, 10) # 749.7 open  1234.8 back
A_i =  two_tube(8.0, 12, 1.0, 10) # 220.5 close 1764.0 front
A_u =  two_tube(5.0, 19, 1.0,  3) # 352.8 close 1278.9 back
A_ae = two_tube(1.0,  6, 8.0, 16) # 661.5 open  1719.9 front

Fs = 44100.0                    # sampling frequency (Hz)
Duration = 1.5                  # duration of generated signal (s)
f0 = 150.0                      # pitch (Hz)

def normalize(s):
    # normalize to unit minus epsilon amplitude
    return 0.99*s/np.amax(np.abs(s))

def varying_pitch(f0, Fs, Duration):
    Fs = 10*Fs                  # upsample
    T = 1/Fs                    # sampling period
    NFT = int(Duration/T)       # number of samples
    t = T*np.arange(NFT)        # time vector
    return (f0+
            100*t/Duration+
            25*np.sin(2*np.pi*t)/Duration+
            0.2*np.sin(2*np.pi*20*t))

def glottal_pulse(Fs, pitch, Duration):
    Fs = 10*Fs                  # upsample
    T = 1/Fs                    # sampling period
    NFT = int(Duration/T)       # number of samples
    t = T*np.arange(NFT)        # time vector
    # half-wave rectify a sine wave
    ug = np.maximum(0, np.sin(2*np.pi*pitch*t))
    # approximate derivative as finite difference, appending zero
    ug = np.concatenate((ug[1:]-ug[:len(ug)-1], np.array([0])))
    ug = np.minimum(0, ug)      # half-wave rectify again
    ug = np.abs(ug)**3          # take power to modify the spectrum
    return normalize(ug)[::10]  # decimate

def impulse():
    return np.array([1000.0]+[0.0]*999) # 1000.0 approximates infinity

def vocal_tract(Fs, A, ug):
    # A model is a sequence of concentric cylinders, represented as an array A
    # of their cross-sectional areas (cm^2). Each cylinder has a length equal to
    # one wavelength of the sampling frequency. For the default parameters this
    # is 0.7936507936507936 cm.
    rho = 0.00114               # density of air
    c = 35000.0                 # speed of sound in air (cm/s)
    # Filter taps are spaced equidistantly a sample wavelength apart. For the
    # forward wave, there is a tap at the end of each cylinder, the last tap
    # being at the lips. For the backward wave, there is a tap at the beginning
    # of each cylinder, the last tap being at the glottis.
    N = len(A)
    # reflection coefficients
    rg = 0.99                                 # at glottis
    rl = -0.99                                # at lips
    r = (A[:N-1]-A[1:])/(A[:N-1]+A[1:])       # at cylinder junctions
    f = np.zeros((N,))          # the taps for the forward wave
    b = np.zeros((N,))          # the taps for the backward wave
    # generated sound sample
    P = []
    # Compute samples.
    for u in ug:
        # The forward wave at the glottis is a mixture of the excitation and
        # the reflection of the backward wave.
        f_input = u*rho*c/A[0]+rg*b[0]
        # The backward wave at the lips is the reflection of the forward wave.
        b_input = rl*f[N-1]
        # scattering at junctions
        delta = r*(f[:N-1]-b[1:])
        # Propagate the forward wave forward.
        f = np.concatenate((np.array([f_input]), f[:N-1]+delta))
        # Propagate the backward wave backward.
        b = np.concatenate((b[1:]+delta, np.array([b_input])))
        # The output is the pressure at the lips.
        P.append(f[N-1])
    return np.array(P)

def play(Fs, P):
    sd.default.samplerate = Fs
    sd.default.channels = 1
    sd.play(normalize(P))
    time.sleep(len(P)/Fs)

def plot_signal(Fs, P):
    plt.cla()
    plt.plot(np.arange(len(P))/Fs, P)
    plt.grid()
    plt.xlabel("time (s)")
    plt.ylabel("Amplitude")
    plt.show(block = False)

def plot_frequency_response(Fs, P):
    points = len(P)
    freq = np.arange(0, points*int(Fs), int(Fs))/float(points)
    yaxis = 20*np.log10(np.abs(np.fft.fft(P)))
    plt.cla()
    plt.plot(freq, yaxis)
    plt.xlim(0, 5000)
    plt.grid()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Frequency response of vocal tract (dB)")
    plt.show(block = False)

def formants(Fs, P):
    points = len(P)
    freq = np.arange(0, points*int(Fs), int(Fs))/float(points)
    yaxis = 20*np.log10(np.abs(np.fft.fft(P)))
    fs = []
    for i in range(1, len(freq)-1):
        if yaxis[i]>yaxis[i-1] and yaxis[i]>yaxis[i+1]:
            fs.append(freq[i])
    return fs

# plot_signal(Fs, impulse())
# plot_signal(Fs, vocal_tract(Fs, A_a, impulse()))
# plot_signal(Fs, vocal_tract(Fs, A_i, impulse()))
# plot_signal(Fs, vocal_tract(Fs, A_u, impulse()))
# plot_signal(Fs, vocal_tract(Fs, A_ae, impulse()))

# plot_frequency_response(Fs, vocal_tract(Fs, A_a, impulse()))
# plot_frequency_response(Fs, vocal_tract(Fs, A_i, impulse()))
# plot_frequency_response(Fs, vocal_tract(Fs, A_u, impulse()))
# plot_frequency_response(Fs, vocal_tract(Fs, A_ae, impulse()))

# formants(Fs, vocal_tract(Fs, A_a, impulse()))[0:2]
# formants(Fs, vocal_tract(Fs, A_i, impulse()))[0:2]
# formants(Fs, vocal_tract(Fs, A_u, impulse()))[0:2]
# formants(Fs, vocal_tract(Fs, A_ae, impulse()))[0:2]

# plot_signal(Fs, glottal_pulse(Fs, f0, Duration))
# plot_frequency_response(Fs, glottal_pulse(Fs, f0, Duration))
# play(Fs, glottal_pulse(Fs, f0, Duration))

# plot_signal(Fs, vocal_tract(Fs, A_a, glottal_pulse(Fs, f0, Duration)))
# plot_signal(Fs, vocal_tract(Fs, A_i, glottal_pulse(Fs, f0, Duration)))
# plot_signal(Fs, vocal_tract(Fs, A_u, glottal_pulse(Fs, f0, Duration)))
# plot_signal(Fs, vocal_tract(Fs, A_ae, glottal_pulse(Fs, f0, Duration)))

# plot_frequency_response(Fs, vocal_tract(Fs, A_a, glottal_pulse(Fs, f0, Duration)))
# plot_frequency_response(Fs, vocal_tract(Fs, A_i, glottal_pulse(Fs, f0, Duration)))
# plot_frequency_response(Fs, vocal_tract(Fs, A_u, glottal_pulse(Fs, f0, Duration)))
# plot_frequency_response(Fs, vocal_tract(Fs, A_ae, glottal_pulse(Fs, f0, Duration)))

# play(Fs, vocal_tract(Fs, A_a, glottal_pulse(Fs, f0, Duration)))
# play(Fs, vocal_tract(Fs, A_i, glottal_pulse(Fs, f0, Duration)))
# play(Fs, vocal_tract(Fs, A_u, glottal_pulse(Fs, f0, Duration)))
# play(Fs, vocal_tract(Fs, A_ae, glottal_pulse(Fs, f0, Duration)))

# plot_signal(Fs, varying_pitch(f0, Fs, Duration))

# plot_signal(Fs, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration))
# plot_frequency_response(Fs, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration))
# play(Fs, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration))

# plot_signal(Fs, vocal_tract(Fs, A_a, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# plot_signal(Fs, vocal_tract(Fs, A_i, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# plot_signal(Fs, vocal_tract(Fs, A_u, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# plot_signal(Fs, vocal_tract(Fs, A_ae, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))

# plot_frequency_response(Fs, vocal_tract(Fs, A_a, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# plot_frequency_response(Fs, vocal_tract(Fs, A_i, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# plot_frequency_response(Fs, vocal_tract(Fs, A_u, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# plot_frequency_response(Fs, vocal_tract(Fs, A_ae, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))

# play(Fs, vocal_tract(Fs, A_a, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# play(Fs, vocal_tract(Fs, A_i, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# play(Fs, vocal_tract(Fs, A_u, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
# play(Fs, vocal_tract(Fs, A_ae, glottal_pulse(Fs, varying_pitch(f0, Fs, Duration), Duration)))
