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

#!/usr/bin/python

import os
import sys
import bigfish_io as bfio
from scipy.fftpack import fft
from scipy.io import wavfile
import time 

# map the FFT output to 2 matrices each with 8 columns of height 8
# FFT ranges from -1 to 1
def map_to_LED_matrix(input_array, steps):
    matrix_lo = [0 for r in range(8)]
    matrix_hi = [0 for r in range(8)]
    #stepsize = len(input_array) // 16
    #for i in range(len(input_array)):
        #if input_array[i] > 1:
            #print ('too large value: ' + str(input_array[i]))
    # get the average value of each subsection of the FFT array, sans the last
    for i in range(16):
        #raw_avg = max_value_in_range(input_array, i * stepsize, (i + 1) * stepsize)
        raw_avg = max_value_in_range(input_array, steps[i], steps[i+1])
        #print (raw_avg)
        fix_avg = (raw_avg * 7) + 1
        #print (fix_avg)
        if(i < 8):
            matrix_lo[i] = int(fix_avg)
        else:
            matrix_hi[i-8] = int(fix_avg)
    #raw_avg = max_value_in_range(input_array, 15 * stepsize, len(input_array) - 1)
    #fix_avg = (raw_avg * 7) + 1
    #matrix_hi[7] = int(fix_avg)
    #print (matrix_lo)
    #print (matrix_hi)
    bfio.updateMatrix(bfio.LOW, matrix_lo)
    bfio.updateMatrix(bfio.HIGH, matrix_hi)


def avg_value_in_range(input_array, start, end):
    sum = 0
    div = end-start
    for i in range(start, end):
        sum += input_array[i]
    sum /= div
    print (sum)
    return sum

def max_value_in_range(input_array, start, end):
    max = -sys.maxsize - 1
    for i in range(start, end):
        if (input_array[i] > max):
            max = input_array[i]
    return max
    
def processaudio(filename):
    timemark = time.time() + 5
    refreshrate = 60 #Hz
    if len(sys.argv) > 2:
        refreshrate = int(sys.argv[2])
    if len(sys.argv) > 3:
        downsample_ratio = int(sys.argv[3])
    bitdepth = 8
    downsample_ratio = 4
    #divisor = 2**bitdepth
    parentpath = os.getcwd()
    filepath = (parentpath + '/audiodownloads/' + filename +'.wav')
    print ('File at: ' + filepath)
    fs, raw = wavfile.read(filepath)
    if (hasattr(raw.T[0], "__len__")):
        raw = raw.T[0]
    #fs /= downsample_ratio
    freqcap = 20000
    print ('Sampling rate (Hz): ' + str(fs))
    numsamples = len(raw) #/ downsample_ratio
    print ('Number of samples: ' + str(numsamples))
    #for i in range(numsamples):
    #    a[i] = (raw[i]/2**bitdepth) * 2 - 1 #normalize to the range [-1,1]
    #a = raw[::downsample_ratio]
    #a=[(ele/2**8.)*2-1 for ele in raw]
    #print('Downsampled length: ' + str(len(a)))
    tracklength = int(numsamples / fs)
    chunklength = int(fs / refreshrate)
    print ('Track length (s): ' + str(tracklength))
    print ('Samples per chunk: ' + str(chunklength))
    highfreq = (freqcap * chunklength) // fs
    startindex = 0
    log_steps = [10, 16.1, 25.9, 41.6, 66.9, 107.5, 172.9, 278.1, 447.2, 719.2, 1156.5, 1859.8, 2990.7, 4809.4, 7733.9, 12437, 20000]
    freq_steps = [int((step * chunklength) // fs) for step in log_steps]
    #input('ready; press enter to start')
    currtime = time.time()
    time.sleep(timemark - currtime)
    #while (currtime < timemark):
    #    currtime = time.time()
    while (startindex + chunklength) < numsamples:
        timemark = time.time() + (1/refreshrate)
        chunk = raw[startindex:(startindex + chunklength)]
        res = fft(chunk)
        spectrum = res[:highfreq]
        #print('Length of spectrum: '+ str(len(spectrum)))
        spectrum = [abs(ele)/numsamples for ele in spectrum]
        map_to_LED_matrix(spectrum, freq_steps)
        startindex += chunklength
        #print(len(spectrum))
        #print(str(len(spectrum)) + '\n' + str(spectrum))
        timecurr = time.time()
        while timecurr < timemark:
            timecurr = time.time()
        #print (timecurr)


def main():
    bfio.initGPIO()
    bfio.clearMatrices()
    print (sys.argv[1])
    processaudio(sys.argv[1])

main()
