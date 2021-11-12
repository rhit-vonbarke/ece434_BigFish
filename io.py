#!/usr/bin/env python3
#chmod +x io.py

#io.py. 
#Purpose: interface with IO
#Uses an 8x8 bicolor LED matrix (with HT16K33 LED Backpack)
#the LED matrix is wired to pins p9.16 (i2c clock), p9.20 (i2c data), Vcc (+3.3V), and Gnd.

import time
import sys
import smbus
import Adafruit_BBIO.GPIO as GPIO


def initGPIO():
	global cButton
	global qButton
	
	global bus
	global matrixAddr
	bus = smbus.SMBus(2)  # Use i2c bus 2
	matrixAddr = 0x70         # Use address 0x70
	
	bus.write_byte_data(matrixAddr, 0x21, 0)   # Start oscillator
	bus.write_byte_data(matrixAddr, 0x81, 0)   # Disp on, blink off
	bus.write_byte_data(matrixAddr, 0xe7, 0)   # Full brightness
	
		
def clearScreen():
	for i in range(16):
		bus.write_byte_data(matrixAddr, i, 0)
		

def updateMatrix():
	#every 2 elements (bytes of data) in matrix array relate to a single column of the matrix (so array[0] and array[1] are associated with leftmost column).
	#For each column, first byte is color red and second byte is color green.
	#For each byte, the bottom of the matrix is associated with the least significant bit and the top of the matrix is associated with the most significant bit.
	
	currentVal = bus.read_byte_data(matrixAddr, 2*x) #argument is: address, byte offset (i hope. could be bit offset. we'll see).
	newVal = currentVal | (1 << y)
	bus.write_byte_data(matrixAddr, 2*x, newVal)
  
  
initGPIO()
