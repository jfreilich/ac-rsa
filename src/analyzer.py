import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
import sys

wavfile = sys.argv[1]
freq_file = sys.argv[2]

# Read wav file
sr,x = scipy.io.wavfile.read(wavfile)
# Read the freq file
freq_file = open(freq_file)
freq_file.next()

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
    if maxA > maxB:
        maxs.append((maxB, maxA))
    else:
        maxs.append((maxA, maxB))

####### BUILD OUR FREQ TO BUTTON MAP ##############
freq_to_button = {}
for line in freq_file:
    line = line.split(",")
    pair = (int(line[0]), int(line[1]))
    button = line[2]
    freq_to_button[pair] = button

####### FIND WHAT WAS PRESSED ######################
buttons = []

found = False
for i in range(len(maxs)):
    if i == 0 or i == len(maxs)-1:
        continue
    if (not found
        and maxs[i] == maxs[i - 1]
        and maxs[i] == maxs[i + 1]
        and maxs[i] in freq_to_button):
        buttons.append(freq_to_button[maxs[i]])
        found = True
    if (maxs[i][0] < 20 and maxs[i][1] < 20
        and maxs[i+1][0] < 20 and maxs[i+1][1]):
        found = False

# Output data
for button in buttons:
    print button.strip()
