# https://docs.scipy.org/doc/scipy/tutorial/fft.html
# https://realpython.com/python-scipy-fft/
# https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html#numpy.fft.fft
# https://realpython.com/python-scipy-fft/


import numpy as np
import matplotlib.pyplot as plt


# Creating signal
Fs=1000                            #Sampling fresquncy
T_inc=1/Fs                         #Time increament
T_measure=1.5                      #Duration of measurment
time=np.arange(0,T_measure,T_inc)     #Vector contains sampling time
L=len(time)                     #Lenght of signal

print(time)


# Sum of a 60Hz and 120 Hz sinusoidal
f1=120;
f2=60;
phi1=1.5;
phi2=2.4;
amplitude1=1.5;
amplitude2=2.2;
y=amplitude1*np.sin(2.*np.pi*f1*time+phi1) + amplitude2*np.sin(2.*np.pi*f2*time+phi2);

# https://docs.scipy.org/doc/scipy/tutorial/fft.html
from scipy.fft import fft, fftfreq



SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y




_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
noise_tone = noise_tone * 0.3

mixed_tone = nice_tone + noise_tone

#normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)
normalized_tone =mixed_tone

plt.plot(normalized_tone[:1000])
plt.show()

from scipy.io.wavfile import write

# Remember SAMPLE_RATE = 44100 Hz is our playback rate
write("mysinewave.wav", SAMPLE_RATE, normalized_tone)



# Number of samples in normalized_tone
N = SAMPLE_RATE * DURATION

yf = fft(normalized_tone)
xf = fftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()


from scipy.fft import rfft, rfftfreq

# Note the extra 'r' at the front
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()



