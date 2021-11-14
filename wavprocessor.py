#!/usr/bin/python

import os
import sys
from scipy.fftpack import fft
from scipy.io import wavfile

# map the FFT output to 2 matrices each with 8 columns of height 8
# FFT ranges from -1 to 1
def map_to_LED_matrix(input_array):
    matrix_lo = [[0 for c in range(8)] for r in range(8)]
    matrix_hi = [[0 for c in range(8)] for r in range(8)]
    stepsize = len(input_array) // 16
    # get the average value of each subsection of the FFT array, sans the last
    for i in range(15):
        raw_avg = avg_value_in_range(input_array, i * stepsize, (i + 1) * stepsize)
        fix_avg = (raw_avg + 1) * 8 // 2
        if(i < 8):
            set_LED_col_height(matrix_lo, i, fix_avg)
        else:
            set_LED_col_height(matrix_hi, i-8, fix_avg)
    raw_avg = avg_value_in_range(input_array, 15 * stepsize, len(input_array) - 1)
    fix_avg = (raw_avg + 1) * 8 // 2
    set_LED_col_height(matrix_hi, 7, fix_avg)


def avg_value_in_range(input_array, start, end):
    return(0)

# TODO: make color functional with green on the bottom 5, yellow on the next two, red on top
def set_LED_col_height(input_matrix, col, height):
    for r in range(8-height, 8):
        input_matrix[r][col] = 1

def processaudio(filename):
    refreshrate = 10 #Hz
    bitdepth = 8
    downsample_ratio = 8
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
    raw = raw[::downsample_ratio]
    a=[(ele/2**8.)*2-1 for ele in raw]
    print('Downsampled length: ' + str(len(a)))
    tracklength = int(numsamples / fs)
    chunklength = int(fs / refreshrate)
    print ('Track length (s): ' + str(tracklength))
    print ('Samples per chunk: ' + str(chunklength))
    startindex = 0
    while (startindex + chunklength) < numsamples:
        chunk = a[startindex:(startindex + chunklength)]
        res = fft(chunk)
        spectrum = res[:len(res)//2 - 1]
        print(len(spectrum))
        spectrum = [abs(ele) for ele in spectrum]
        startindex += chunklength
        print(len(spectrum))
        #print(str(len(spectrum)) + '\n' + str(spectrum))


def main():
    print (sys.argv[1])
    processaudio(sys.argv[1])

main()
