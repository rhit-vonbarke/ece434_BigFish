import numpy as np

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

