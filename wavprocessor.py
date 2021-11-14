#!/usr/bin/python

import os
import sys
import bigfish_io as bfio
from scipy.fftpack import fft
from scipy.io import wavfile
import time 

# map the FFT output to 2 matrices each with 8 columns of height 8
# FFT ranges from -1 to 1
def map_to_LED_matrix(input_array):
    matrix_lo = [0 for r in range(8)]
    matrix_hi = [0 for r in range(8)]
    stepsize = len(input_array) // 16
    #for i in range(len(input_array)):
        #if input_array[i] > 1:
            #print ('too large value: ' + str(input_array[i]))
    # get the average value of each subsection of the FFT array, sans the last
    for i in range(15):
        raw_avg = max_value_in_range(input_array, i * stepsize, (i + 1) * stepsize)
        #print (raw_avg)
        fix_avg = raw_avg * 8
        #print (fix_avg)
        if(i < 8):
            matrix_lo[i] = int(fix_avg)
        else:
            matrix_hi[i-8] = int(fix_avg)
    raw_avg = max_value_in_range(input_array, 15 * stepsize, len(input_array) - 1)
    fix_avg = (raw_avg + 1) * 8 // 2
    matrix_hi[7] = int(fix_avg)
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
    refreshrate = 15 #Hz
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
    fs /= downsample_ratio
    print ('Sampling rate (Hz): ' + str(fs))
    numsamples = len(raw) / downsample_ratio
    print ('Number of samples: ' + str(numsamples))
    #for i in range(numsamples):
    #    a[i] = (raw[i]/2**bitdepth) * 2 - 1 #normalize to the range [-1,1]
    a = raw[::downsample_ratio]
    #a=[(ele/2**8.)*2-1 for ele in raw]
    print('Downsampled length: ' + str(len(a)))
    tracklength = int(numsamples / fs)
    chunklength = int(fs / refreshrate)
    print ('Track length (s): ' + str(tracklength))
    print ('Samples per chunk: ' + str(chunklength))
    startindex = 0
    input('ready; press enter to start')
    while (startindex + chunklength) < numsamples:
        timemark = time.time() + (1/refreshrate)
        chunk = a[startindex:(startindex + chunklength)]
        res = fft(chunk)
        spectrum = res[:len(res)//2 - 1]
        #print('Length of spectrum: '+ str(len(spectrum)))
        spectrum = [abs(ele)/numsamples for ele in spectrum]
        map_to_LED_matrix(spectrum)
        startindex += chunklength
        #print(len(spectrum))
        #print(str(len(spectrum)) + '\n' + str(spectrum))
        timecurr = time.time()
        while timecurr < timemark:
            timecurr = time.time()
        print (timecurr)


def main():
    bfio.initGPIO()
    bfio.clearMatrices()
    print (sys.argv[1])
    processaudio(sys.argv[1])

main()
