import sys
import wave
import scipy as sp
import scipy.fftpack
import numpy as np
import matplotlib.pyplot as plt
from pytfd.stft import *
from pytfd import windows

def main():
   if len(sys.argv) != 2:
      print "usage: python ac.py <audio_file>"
   else:
      # Open the .wav file
      wav_file = wave.open(sys.argv[1], 'r')
      # assumes that it is 1 channel
      assert wav_file.getnchannels() == 1, ".wav is not single channel."
      # get some basic information about the wav
      sample_rate = wav_file.getframerate()
      frame_size = 1.0/sample_rate
      num_frames = wav_file.getnframes()
      int_size = wav_file.getsampwidth()
      # read the wave into a np.array of amplitude values
      wav = np.frombuffer(wav_file.readframes(num_frames),
                           # Adjust how big the integers are based on wav
                           'i' + str(int_size))
      wav_file.close()
      # Get array of times associated with each amplitude value
      wav_times = get_times(num_frames, frame_size)
#      # Get FFT, array of amplitudes for each frequency value
#      wav_fft = abs(sp.fft(wav))
#      # Get the associated frequencies
#      wav_freqs = scipy.fftpack.fftfreq(wav.size, frame_size)
#      # Graph everything
#      graph_frequencies(wav, wav_times, wav_freqs, wav_fft)
      #t = sp.linspace(0, 5, 5*8000, endpoint=False)
      #x = sp.sin(2*sp.pi*440*t)
      #wav_stft = stft(x, 8000, 0.050, 0.020)
      w = windows.rectangular(8)
      wav_stft = stft(wav, w, L=64)
      graph_stft(wav_stft)

# Given number of frames, and how often they were sampled
# return an array of times for those frames.
def get_times(num_frames, frame_size):
   times = []
   # time = index_in_array*frame_size
   for i in range(num_frames):
      times.append(i * frame_size)
   return times

# def stft(x, fs, framesz, hop):
#     framesamp = int(framesz*fs)
#     hopsamp = int(hop*fs)
#     w = sp.hamming(framesamp)
#     X = sp.array([sp.fft(w*x[i:i+framesamp]) 
#                   for i in range(0, len(x)-framesamp, hopsamp)])
#     return X

def graph_frequencies(wav, times, freqs, fft):
   # Plot Amplitude wave
   plt.subplot(211)
   plt.plot(times, wav)
   plt.title("Amplitude vs. Time")
   plt.xlabel("Time (s)")
   plt.ylabel("Amplitude (dB)")
   # Plot FFT
   plt.subplot(212)
   plt.plot(freqs, 20*sp.log10(fft), 'x')
   plt.title("Magnitude vs. Frequency (Hz)")
   plt.xlabel("Frequency (Hz)")
   plt.ylabel("Magnitude (Y)")
   plt.xlim(0)
   #plt.xlim(20000,23000)
   #plt.ylim(40,90)
   plt.savefig("wave.png")
   plt.show()

def graph_stft(stft):
   plt.figure()
   plt.imshow(sp.absolute(stft.T), origin='lower', aspect='auto',
             interpolation='nearest')
   plt.xlabel("Time")
   plt.ylabel("Frequency")
   plt.ylim(0)
   plt.show()

if __name__ == '__main__':
    main()
