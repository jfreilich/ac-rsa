import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
import sys

wavfile = sys.argv[1]

# Read wav file
sr,x = scipy.io.wavfile.read(wavfile)

######## STFT #####################################

# Parameters: 10ms step, 30ms window
nstep = int(sr * 0.01)
nwin  = int(sr * 0.03)
nfft = nwin

window = np.hamming(nwin)

# will take windows x[n1:n2].  generate
# and loop over n2 such that all frames
# fit within the waveform
nn = range(nwin, len(x), nstep)

X = np.zeros( (len(nn), nfft/2) )

for i,n in enumerate(nn):
    xseg = x[n-nwin:n]
    z = np.fft.fft(window * xseg, nfft)
    X[i,:] = np.log(np.abs(z[:nfft/2]))

###################################################

####### EXTRACT TONES #############################

# how far away in index the two max tones should be from eachother
threshold = 2
# list of max tuples, two max values for each point in time.
maxs = []
for frequencies in np.transpose(X.T):
    maxA = 0
    maxB = 0
    # find the first max
    maxA = np.amax(frequencies)
    maxA = frequencies.tolist().index(maxA)
    # find the second match at least threshold index away
    i = 0
    maxB = 0
    for i in range(len(frequencies)):
        if abs(i - maxA) < threshold:
            continue
        amp = frequencies[i]
        if amp > frequencies[maxB]:
            maxB = i
    if maxA > 20 or maxB > 20:
        if maxA > maxB:
            maxs.append((maxB, maxA))
        else:
            maxs.append((maxA, maxB))

####### CLEAN DATA #################################
cleaned = []
# remove singleton data points
for i in range(len(maxs)):
    if i == 0 or i == len(maxs)-1:
        continue
    if maxs[i] == maxs[i - 1] and maxs[i] == maxs[i + 1]:
        cleaned.append(maxs[i])
# remove duplicate values, while keeping order
def remove_dups(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
cleaned = remove_dups(cleaned)

# Output data
for tone in cleaned:
    print tone

# Show spectrogram
plt.imshow(X.T, interpolation='nearest',
    origin='lower',
    aspect='auto')
plt.ylim(0,100)
plt.show()

