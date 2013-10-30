#!/usr/bin/env python

import serial
import time

from CRC16 import calcString
from xml.dom import minidom

# SERIAL PC CONFIG.
ser = serial.Serial(port='COM2',baudrate=19200)

# FUNCTIONS
# Decimal to Hex.
def dec2hex(n):
	lo = n & 0x00FF
	hi = (n & 0xFF00) >> 8
	return chr(hi) + chr(lo)
	#return "%02x" % n

# Hex. to Decimal
def hex2dec(s):
    return int(s, 16)

# Invert byte ( LO and HI )
def swapLoHi(n):
    lo = n & 0x00FF
    hi = (n & 0xFF00) >> 8
    return  lo << 8 | hi

# Calc. CRC16
def stCRC(msg):
    crc = calcString(msg, 0xFFFF)
    crc = swapLoHi(crc)
    return dec2hex(crc)
	

def HiLo(n):
    lo = n & 0x00FF
    hi = (n & 0xFF00) >> 8
    return  hi | lo
	
# MODBUS PROTOCOL DEFINES
READ_HOLDING = 3
READ_INPUT = 4
PRESET_SINGLE = 6
PRESET_MULTIPLE = 10
		
# INPUT VALUES
nb = input('Power: ')
nc = input('Forward Power: ')
nd = input('Reflected Power: ')
ne = input('Temp: ')

# CONVERT VALUE TO STRING HEX
power =  chr(nb)	
forward = chr(nc)
reflected = chr(nd)
temp = chr(ne)

### DEBUG MSG. ###
#ReadHolding = "\x01\x03\x02\x00" + power + "\x01\x0a"
ReadHolding = "\x01\x03\x02\x00" + power
stMsg = ReadHolding + stCRC(ReadHolding)
ReadInput1 = "\x02\x04\x02\x00" + forward + "\x00"+ reflected +"\x84"
ReadInput2 = "\x03\x04\x02\x00" + reflected + "\x00\x0a\x84" 
PresetSingle1 = "\x01\x06\x00\x00\x00\x0A"
PresetMultiple1 = "\x01\x10\x70\x00\x06"
PresetMultiple = PresetMultiple1 + stCRC(PresetMultiple1)
PresetSingle = PresetSingle1 + stCRC(PresetSingle1)

## LOOP MODBUS
while True:
	out = ''
# let's wait one second before reading output (let's give device time to answer)
	time.sleep(1)
	
# MODBUS READ BUFFER
	while ser.inWaiting() > 0:
		out += ser.read(1)

### DEBUG ###
	if out != '':
		print "uC Response"
		print out[0].encode('hex_codec') 
		print out[1].encode('hex_codec') 
		print out[2].encode('hex_codec')
		print out[3].encode('hex_codec')
		print out[4].encode('hex_codec')
		print out[5].encode('hex_codec')
		print out[6].encode('hex_codec')
		print out[7].encode('hex_codec')

# GET PROTOCOL
	value = int(out[1].encode('hex_codec'),16)
	print value 

# READ HOLDING MSG.
	if value is READ_HOLDING:
		print "read holding"
		nb = nb + 1
		if nb is 255:
			nb = 1
		power =  chr(nb)
		ReadHolding = "\x01\x03\x02\x00" + power
		stMsg = ReadHolding + stCRC(ReadHolding)
		ser.write(stMsg)
		time.sleep(1) # for 100 millisecond delay
		
# READ INPUT MSG.
	elif value is READ_INPUT:
		print "read input"
		nc = nc + 1
		nd = nd + 1
		ne = ne + 1
		
		if nc is 255:
			nc = 1
		if nd is 255:
			nd = 1
		if ne is 255:
			ne = 1
			
		forward = chr(nc)
		reflected = chr(nd)
		temp = chr(ne)
		#ReadInput1 = "\x01\x04\x04\x00" + forward + "\x00"+ reflected
		ReadInput1 = "\x01\x04\x22\x00" + forward + "\x00"+ reflected + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp + "\x00" + temp
		stMsg1 = ReadInput1 + stCRC(ReadInput1)
		ser.write (stMsg1)
		time.sleep(1) #for 100 millisecond delay

# PRESET SINGLE MSG.
	elif value is PRESET_SINGLE:
		print "preset single"
		val = int(out[5].encode('hex_codec'),16)
		power = chr(val) # debug pot.
		ser.write (PresetSingle)
		
				
# PRESET MULTIPLE MSG.
	elif value is PRESET_MULTIPLE:
		print "preset multiple"
		ser.write (PresetMultiple)
		time.sleep(1) # for 100 millisecond delay
		
	RecievedData = ""

	#while ser.inWaiting() > 0:
	#    RecievedData = ser.read(1)
	#print RecievedData
