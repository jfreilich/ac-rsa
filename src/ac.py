import sys
import wave
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import fourier

def main():
   if len(sys.argv) != 2:
      print "usage: python ac.py <audio_file>"
   else:
      # Open the .wav file
      wav_file = wave.open(sys.argv[1], 'r')
      # assumes that it is 1 channel with int16 data.
      assert wav_file.getnchannels() == 1, ".wav is not single channel."
      # read the entire .wav file into an array of amplitude values.
      num_frames = wav_file.getnframes()
      wav = np.frombuffer(wav_file.readframes(num_frames), 'i' + str(wav_file.getsampwidth()))
      # use fft to transform into frequency wave.
      sample_rate = wav_file.getframerate()
      frame_size = 1.0/sample_rate
      wav_length =  frame_size*num_frames
      wav_transform = fourier.fft(wav)
      # get the time function
      wav_times = get_times(wav_transform, sample_rate)
      # graph the wave
      graph_frequencies(wav_times, wav_transform)

def get_times(samples, sample_rate):
   times = []
   # time = index_in_array*time_multiplier
   time_multiplier = 1.0/sample_rate
   for i in range(len(samples)):
      times.append(i * time_multiplier)
   return times

def graph_frequencies(wav_times, wav_frequencies):
   plt.plot(wav_times, wav_frequencies)
   plt.title("Frequency vs Time")
   plt.xlabel("Time")
   plt.ylabel("Frequency")
   plt.show()


if __name__ == '__main__':
    main()
