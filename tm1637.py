import sys
import time
import os
import machine
from machine import Pin as PIN

HexDigits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7
OUTPUT = PIN.OUT
INPUT = PIN.IN
LOW = 0
HIGH = 1

class tm1637:
	__doublePoint = False
	__Clkpin = 0
	__Datapin = 0
	__Clkpin_nr = 0
	__Datapin_nr = 0
	__brightnes = BRIGHT_TYPICAL;
	__currentData = [0,0,0,0];
	
	def __init__( self, pinClock, pinData, brightnes ):
		self.__Clkpin_nr = pinClock
		self.__Datapin_nr = pinData
		self.__brightnes = brightnes;
		self.__Clkpin = PIN(self.__Clkpin_nr,OUTPUT)
		self.__Datapin = PIN(self.__Datapin_nr,OUTPUT)
	# end  __init__

	def Clear(self):
		b = self.__brightnes;
		point = self.__doublePoint;
		self.__brightnes = 0;
		self.__doublePoint = False;
		data = [0x7F,0x7F,0x7F,0x7F];
		self.Show(data);
		self.__brightnes = b;				# restore saved brightnes
		self.__doublePoint = point;
	# end  Clear

	def Show( self, data ):
		for i in range(0,4):
			self.__currentData[i] = data[i];
		
		self.start();
		self.writeByte(ADDR_AUTO);
		self.stop();
		self.start();
		self.writeByte(STARTADDR);
		for i in range(0,4):
			self.writeByte(self.coding(data[i]));
		self.stop();
		self.start();
		self.writeByte(0x88 + self.__brightnes);
		self.stop();
	# end  Show

	def Show1(self, DigitNumber, data):	# show one Digit (number 0...3)
		if( DigitNumber < 0 or DigitNumber > 3):
			return;	# error
	
		self.__currentData[DigitNumber] = data;
		
		self.start();
		self.writeByte(ADDR_FIXED);
		self.stop();
		self.start();
		self.writeByte(STARTADDR | DigitNumber);
		self.writeByte(self.coding(data));
		self.stop();
		self.start();
		self.writeByte(0x88 + self.__brightnes);
		self.stop();
	# end  Show1
		
	def SetBrightnes(self, brightnes):		# brightnes 0...7
		if( brightnes > 7 ):
			brightnes = 7;
		elif( brightnes < 0 ):
			brightnes = 0;

		if( self.__brightnes != brightnes):
			self.__brightnes = brightnes;
			self.Show(self.__currentData);
		# end if
	# end  SetBrightnes

	def ShowDoublepoint(self, on):			# shows or hides the doublepoint
		if( self.__doublePoint != on):
			self.__doublePoint = on;
			self.Show(self.__currentData);
		# end if
	# end  ShowDoublepoint
			
	def writeByte( self, data ):
		for i in range(0,8):
			self.__Clkpin.value(LOW)
			if(data & 0x01):
				self.__Datapin.value(HIGH)
			else:
				self.__Datapin.value(LOW)
			data = data >> 1
			self.__Clkpin.value(HIGH)
		#endfor

		# wait for ACK
		self.__Clkpin.value(LOW)
		self.__Datapin.value(HIGH)
		self.__Clkpin.value(HIGH)
		self.__Datapin = PIN(self.__Datapin_nr, INPUT)
		
		while(self.__Datapin.value()):
			time.sleep(0.001)
			if( self.__Datapin.value()):
				self.__Datapin = PIN(self.__Datapin_nr, OUTPUT)
				self.__Datapin.value(LOW)
				self.__Datapin = PIN(self.__Datapin_nr, INPUT)
			#endif
		# endwhile            
		self.__Datapin = PIN(self.__Datapin_nr, OUTPUT)
	# end writeByte
    
	def start(self):
		self.__Clkpin.value(HIGH) # send start signal to TM1637
		self.__Datapin.value(HIGH)
		self.__Datapin.value(LOW) 
		self.__Clkpin.value(LOW) 
	# end start
	
	def stop(self):
		self.__Clkpin.value(LOW) 
		self.__Datapin.value(LOW) 
		self.__Clkpin.value(HIGH)
		self.__Datapin.value(HIGH)
	# end stop
	
	def coding(self, data):
		if( self.__doublePoint ):
			pointData = 0x80
		else:
			pointData = 0;
		
		if(data == 0x7F):
			data = 0
		else:
			data = HexDigits[data] + pointData;
		return data
	# end coding
	
# end class TM1637
