#!/usr/bin/python

import os
import sys
import bigfish_io as bfio
from scipy.fftpack import fft
from scipy.io import wavfile
import time
import subprocess

# maximum amplitude to adjust spectrum values
amp_max = 0.1


# logarithmically maps the fft 'input_array' into 16 buckets with ranges defined by 'steps'
def map_to_LED_matrix(input_array, steps):
    global amp_max
    pass_max = 0
    matrix_lo = [0 for r in range(8)]
    matrix_hi = [0 for r in range(8)]
    for i in range(16):
        raw_avg = max_value_in_range(input_array, steps[i], steps[i+1])
        if(raw_avg > pass_max):
            pass_max = raw_avg
        if(raw_avg > amp_max):
            amp_max = raw_avg
        fix_avg = ((raw_avg/amp_max) * 7) + 1
        if(i < 8):
            matrix_lo[i] = int(fix_avg)
        else:
            matrix_hi[i-8] = int(fix_avg)
    if(pass_max < (0.5*amp_max)):
        amp_max = (pass_max + 9*amp_max)/10 #weighted average to slowly reduce ceiling if song drops in amplitude

    bfio.updateMatrix(bfio.LOW, matrix_lo)
    bfio.updateMatrix(bfio.HIGH, matrix_hi)

# maps amplitude within human vocal range defined by 'mrange' and 'frange' to servo positions
def map_to_servo(input_array, mrange, frange):
    global amp_max
    val = 0
    maxm = max_value_in_range(input_array, mrange[0], mrange[1])
    maxf = max_value_in_range(input_array, frange[0], frange[1])
    if(abs(maxm) > abs(maxf)):
        val = maxm
    else:
        val = maxf
    val = (val/amp_max) * 2 - 1
    if(abs(val) > 1):
        val = val/abs(val)
    bfio.updateServo(val)

# returns the highest value in an array between start and end
def max_value_in_range(input_array, start, end):
    max = -sys.maxsize - 1
    for i in range(start, end):
        if (input_array[i] > max):
            max = input_array[i]
    return max

# main code; processes audio one chunk at a time and feeds values to 
# matrix and servo mapping code, uses time reference to maintain 
# specific constant refresh rate
def processaudio(filename):
    global playproc
    timemark = (int(sys.argv[2])/1000000000) + 10 # this value needs to be higher for extremely long videos
    refreshrate = 60 #Hz
    bitdepth = 8
    parentpath = os.getcwd()
    filepath = (parentpath + '/audiodownloads/' + filename +'.wav')
    print ('File at: ' + filepath)
    fs, raw = wavfile.read(filepath)
    # if track isn't mono, select first channel
    if (hasattr(raw.T[0], "__len__")):
        raw = raw.T[0]
    numsamples = len(raw)
    tracklength = int(numsamples / fs)
    chunklength = int(fs / refreshrate)
    print ('Sampling rate (Hz): ' + str(fs))
    print ('Track length (s): ' + str(tracklength))
    # define max frequency, and log steps from 10 to max frequency
    freqcap = 20000
    highfreq = (freqcap * chunklength) // fs
    startindex = 0
    log_steps = [10, 16.1, 25.9, 41.6, 66.9, 107.5, 172.9, 278.1, 447.2, 719.2, 1156.5, 1859.8, 2990.7, 4809.4, 7733.9, 12437, 20000]
    # convert steps to bin numbers in FFT array
    freq_steps = [int((step * chunklength) // fs) for step in log_steps]
    # ensure different log sections have different start/end values
    for i in range (1,len(freq_steps)):
        if (freq_steps[i] <= freq_steps[i-1]):
            freq_steps[i] = freq_steps[i-1] + 1
    # convert human voice range arrays as well
    mvoice = [85, 155]
    freq_mvoice = [int((step * chunklength) // fs) for step in mvoice]
    fvoice = [165, 255]
    freq_fvoice = [int((step * chunklength) // fs) for step in fvoice]
    currtime = time.time()
    iter = 4
    # wait out remaining time
    time.sleep(timemark - currtime)
    while (currtime < timemark):
        currtime = time.time()
    while (startindex + chunklength) < numsamples:
        # keep track of time to ensure consistent framerate
        timemark = time.time() + (1/refreshrate)
        # isolate specific time slice of audio, then FFT it
        chunk = raw[startindex:(startindex + chunklength)]
        res = fft(chunk)
        spectrum = res[:highfreq]
        spectrum = [abs(ele)/numsamples for ele in spectrum]
        startindex += chunklength
        # do matrix code
        map_to_LED_matrix(spectrum, freq_steps)
        # only update servo every 4 iterations, otherwise doesn't work
        iter -= 1
        if(iter == 0):
            iter = 4
            map_to_servo(spectrum, freq_mvoice, freq_fvoice)
        # go into waiting loop until next 'frame'
        timecurr = time.time()
        while timecurr < timemark:
            timecurr = time.time()

def main():
    bfio.initGPIO()
    bfio.clearMatrices()
    processaudio(sys.argv[1])

main()
