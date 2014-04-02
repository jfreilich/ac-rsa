import scipy.io.wavfile
import numpy as np
import sys
from pylab import *

wavfile = sys.argv[1]
sr, x = scipy.io.wavfile.read(wavfile)

NFFT = 1024       # the length of the windowing segments

# Pxx is the segments x freqs array of instantaneous power, freqs is
# the frequency vector, bins are the centers of the time bins in which
# the power is computed, and im is the matplotlib.image.AxesImage
# instance

Pxx, freqs, bins, im = specgram(x, NFFT=NFFT, Fs=sr, noverlap=900,
                                        cmap=cm.gist_heat)
ylim(0, 2500)
show()
