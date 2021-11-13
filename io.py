#!/usr/bin/env python3
#chmod +x io.py

#io.py. 
#Purpose: interface with IO
#Uses two 8x8 bicolor LED matricies (with HT16K33 LED Backpack)
#The first LED matrix is used to visualize low frequencies. It is wired to pins p9.24 (i2c clock), p9.26 (i2c data), Vcc (+3.3V), and Gnd. It uses I2C1.
#The second LED matrix is used to visualize high frequencies. It is wired to pins p9.19 (i2c clock), p9.20 (i2c data), Vcc (+3.3V), and Gnd. It uses I2C2.

import time
import sys
import smbus
import Adafruit_BBIO.GPIO as GPIO


#"constants"
LOW = 0
HIGH = 1

RED_BITMASK = 0b11100000
GREEN_BITMASK = 0b01111111

def initGPIO():
	global matrixAddr
	global buses
	buses = [smbus.SMBus(1), smbus.SMBus(2)]
	matrixAddr = 0x70         # Use address 0x70
	
	global newMatrixVals
	newMatrixVals = [0] * 16
	
	for bus in buses:
		bus.write_byte_data(matrixAddr, 0x21, 0)   # Start oscillator
		bus.write_byte_data(matrixAddr, 0x81, 0)   # Disp on, blink off
		bus.write_byte_data(matrixAddr, 0xe7, 0)   # Full brightness
	
	clearMatrices()
	updateMatrix(LOW, [0, 0, 5, 8, 6, 0, 0, 0])
	
		
def clearMatrices():
	for bus in buses:
		for i in range(16):
			bus.write_byte_data(matrixAddr, i, 0)
		
		
def updateMatrix(matrix, values = []):
	#every 2 elements (bytes of data) in matrix array relate to a single column of the matrix (so array[0] and array[1] are associated with leftmost column).
	#For each column, first byte is color red and second byte is color green.
	#For each byte, the bottom of the matrix is associated with the least significant bit and the top of the matrix is associated with the most significant bit.
	#currentVal = bus.read_byte_data(matrixAddr, 2*x) #argument is: address, byte offset (i hope. could be bit offset. we'll see).
	#newVal = currentVal | (1 << y)
	#bus.write_byte_data(matrixAddr, 2*x, newVal)
	for k in range(len(values)):
		newVal = getValFromHeight(values[k])
		newMatrixVals[2*k] = RED_BITMASK & newVal
		newMatrixVals[2*k+1] = GREEN_BITMASK & newVal
	buses[matrix].write_block_data(matrixAddr, 0, newMatrixVals)
	
  
def getValFromHeight(value):
	print("Getting val from height")
	print("/n")
	print(value)
	if (value == 0):
		return 0b0
	binNum = 0b1
	for k in range(value):
		binNum = binNum << 1
		binNum = binNum | 1
	print("/n")
	print(value)
	return binNum


  
initGPIO()
