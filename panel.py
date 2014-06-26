from time import sleep
import pygame.mixer
import serial 
import subprocess
import threading

serialFromArduino = serial.Serial("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_649363330373519180D0-if00", 115200)
serialFromArduino.flush()

sleep(5)
pygame.mixer.pre_init(48000, -16, 2, 1024) #was 1024
pygame.mixer.init()
warning = False

cws = pygame.mixer.Sound("/home/pi/space/cws.wav")
cws.set_volume(0.2)
cwsC = pygame.mixer.Channel(1)
thirteenSound = pygame.mixer.Sound("/home/pi/space/11event.wav")

teiPushed = 0
spsPushed = 0
suitCompPushed = 0
abortArmed = 0
lightningStruck = 0
sceRestored = False
sceAux = False
cwsPower = False
thirteen = False

def lightningStrike():
	global lightningStruck
	global sceAux
	#lightningStruck = 1
	while True:
		if (lightningStruck == 1):
			if not sceAux:
				serialFromArduino.write(b'1,4,4,1,1\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(2)
			if not sceAux:		
				serialFromArduino.write(b'1,4,4,2,5\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(2)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,2,0\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,0,5\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,1,3\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(2)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,2,1\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,2,3\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,2,4\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,0,2\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,1,2\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,2,2\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,1,4\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
				sleep(1)
			if not sceAux:
				serialFromArduino.write(b'1,4,4,0,1\n')
				sleep(0.1)
				serialFromArduino.write(b'1,4,4,3,6\n')
				cwsC.play(cws)
			lightningStruck = 0
			sleep(1)

def sceRestore():
	global sceRestored
	while True:
		if sceRestored:
			cwsC.stop()
			serialFromArduino.write(b'0,4,4,1,1\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,2,5\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,2,0\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,0,5\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,1,3\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,2,1\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,2,3\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,2,4\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,0,2\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,1,2\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,2,2\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,1,4\n')
			sleep(0.1)
			serialFromArduino.write(b'0,4,4,0,1\n')
			sceRestored = False
		sleep(0.5)

def thirteenEvent():
	global thirteen
	global thirteenSound
	global cwsC
	global cws
	while True:
		if thirteen:
			serialFromArduino.write(b'1,4,4,3,0\n') # Light next to switch
			offbit = 0
			thirteenSound.play()
			sleep(4.7)
		#	serialFromArduino.write(b'1,4,4,1,5\n') # Ox flow high
		#	sleep(0.1)
		#	serialFromArduino.write(b'1,4,4,3,6\n') # Illuminated Master Alarm Pushbutton
		#	cwsC.play(cws)
		#	sleep(0.1)
		#	serialFromArduino.write(b'2,11,0,0,0\n')
		#	sleep(1)
		#	serialFromArduino.write(b'2,10,0,0,0\n')
		#	sleep(1)
			serialFromArduino.write(b'2,9,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,9,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,8,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,8,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'1,4,4,2,2\n')	# Main Bus B Undervolt
			sleep(0.1)
			serialFromArduino.write(b'1,4,4,3,6\n') # Illuminated Master Alarm Pushbutton
			cwsC.play(cws)
			sleep(0.5)
	
			serialFromArduino.write(b'2,7,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,7,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,6,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,6,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,5,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,5,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,4,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,4,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,3,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,3,6,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,2,0,0,0\n')
			sleep(0.5)
			serialFromArduino.write(b'2,2,6,0,0\n')
			sleep(0.5)
			thirteen = False
		sleep(0.1)

def mainLoop():

	global teiPushed
	global spsPushed
	global suitCompPushed
	global abortArmed
	global lightningStruck
	global sceAux
	global sceRestored
	global airComp
	global cws
	global cwsPower
	global thirteen
	
	tliPushed = 0
	sicPushed = 0
	siiPushed = 0
	sivbPushed = 0
	miPushed = 0
	miiPushed = 0
	miiiPushed = 0
	glycolPushed = 0
	
	aborted = pygame.mixer.Sound("/home/pi/space/aborted.wav")
	liftoff = pygame.mixer.Sound("/home/pi/space/liftoff.wav")
	stagetwo = pygame.mixer.Sound("/home/pi/space/stagetwo.wav")
	stagethree = pygame.mixer.Sound("/home/pi/space/stagethree.wav")
	switchorbits = pygame.mixer.Sound("/home/pi/space/switchorbits.wav")
	tde = pygame.mixer.Sound("/home/pi/space/tde.wav")
	landeva = pygame.mixer.Sound("/home/pi/space/landeva.wav")
	headhome = pygame.mixer.Sound("/home/pi/space/headhome.wav")
	reentry = pygame.mixer.Sound("/home/pi/space/reentry.wav")
	splashdown = pygame.mixer.Sound("/home/pi/space/splashdown.wav")
	poll = pygame.mixer.Sound("/home/pi/space/poll.wav")

	sequenceC = pygame.mixer.Channel(2)
	
	shortexp = pygame.mixer.Sound("/home/pi/space/shortexp.wav")
	medexp = pygame.mixer.Sound("/home/pi/space/medexp.wav")
	les = pygame.mixer.Sound("/home/pi/space/les.wav")
	pexp = pygame.mixer.Sound("/home/pi/space/pexp.wav")
	hiexp = pygame.mixer.Sound("/home/pi/space/hiexp.wav")
	drogue = pygame.mixer.Sound("/home/pi/space/drogue.wav")
	main = pygame.mixer.Sound("/home/pi/space/main.wav")
	fpump = pygame.mixer.Sound("/home/pi/space/fpump.wav")
	fpump.set_volume(0.7)
	fan = pygame.mixer.Sound("/home/pi/space/fan.wav")
	heat = pygame.mixer.Sound("/home/pi/space/heat.wav")
	sps = pygame.mixer.Sound("/home/pi/space/sps.wav")
	tei = pygame.mixer.Sound("/home/pi/space/tli.wav")
	tli = pygame.mixer.Sound("/home/pi/space/tli.wav")
	sic = pygame.mixer.Sound("/home/pi/space/sii.wav")
	sii = pygame.mixer.Sound("/home/pi/space/sii.wav")
	sivb = pygame.mixer.Sound("/home/pi/space/sivb.wav")
	mi = pygame.mixer.Sound("/home/pi/space/mi.wav")
	mii = pygame.mixer.Sound("/home/pi/space/mii.wav")
	miii = pygame.mixer.Sound("/home/pi/space/miii.wav")
	flush = pygame.mixer.Sound("/home/pi/space/flush.wav")
	aircomp = pygame.mixer.Sound("/home/pi/space/aircomp.wav")
	aircomp.set_volume(0.5)
	dieselpump = pygame.mixer.Sound("/home/pi/space/dieselpump.wav")
	dieselpump.set_volume(0.7)
	extend = pygame.mixer.Sound("/home/pi/space/extend.wav")
	retract = pygame.mixer.Sound("/home/pi/space/retract.wav")
	qin = pygame.mixer.Sound("/home/pi/space/qin.wav")
	qin.set_volume(0.3)
	qout = pygame.mixer.Sound("/home/pi/space/qout.wav")
	qout.set_volume(0.3)
	hflow = pygame.mixer.Sound("/home/pi/space/lantern.wav")
	cfan = pygame.mixer.Sound("/home/pi/space/cfan.wav")
	cfan.set_volume(0.3)
	#explosion = pygame.mixer.Sound("explosion")
	#engine = pygame.mixer.Sound("engine.wav")
	
	serialFromArduino.write(b'0,4,4,6,0\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,6,1\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,6,2\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,6,3\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,6,4\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,7,0\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,7,1\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,7,2\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,7,3\n')
	sleep(0.1)
	serialFromArduino.write(b'0,4,4,7,4\n')

	print "System Ready."

	# Loop while waiting for a keypress
	while True:
		try:
			digit = ord(serialFromArduino.read())
			offBit = 0
#			 if (digit < 128):
				#print(digit)
			if (digit > 127):
				digit = digit - 128
				#print digit, "off"
				offBit = 1
			if (digit == 25):
				if (offBit):
					offBit = 0
					medexp.play()
			elif (digit == 14): # Abort button
				if (offBit):
					offBit = 0
				else:
					if abortArmed:
						aborted.play()
						serialFromArduino.write(b'0,4,4,7,5\n')
						subprocess.call("halt", shell=True)
			elif (digit == 3): #Master Alarm button
				if (offBit):
					offBit = 0
				else:
					cwsC.stop()
					serialFromArduino.write(b'0,4,4,3,6\n')
					warning = False

			elif (digit == 6):
				if (offBit):
					cwsPower = False
					serialFromArduino.write(b'1,4,4,2,1\n')
					sleep(0.1)
					cwsC.play(cws)
					serialFromArduino.write(b'1,4,4,3,6\n')
				else:
					offBit = 0
					cwsPower = True
					serialFromArduino.write(b'0,4,4,2,1\n')
					cwsC.stop()
			elif (digit == 5): #                      Initiate Apollo 12 Lightning Strike
				if (offBit):
					offBit = 0
				else:
					if not cwsPower:
						if not lightningStruck:
							#global sceAux
							if not sceAux:
								lightningStruck = 1
			elif (digit == 26):
				if (offBit):
					offBit = 0
					hiexp.play()
			elif (digit == 27):
				if (offBit):
					main.play()
					serialFromArduino.write(b'1,4,4,0,4\n')
				else:
					offBit = 0
			if (digit == 24):
				if (offBit):
					les.play()
				else:
					offBit = 0
			elif (digit == 30):
				if (offBit):
					drogue.play()
					serialFromArduino.write(b'1,4,4,0,5\n')
				else:
					offBit = 0
			if (digit == 29):
				if (offBit):
					offBit = 0
					pexp.play()
			elif (digit == 28):
				if (offBit):
					offBit = 0
					shortexp.play()
			elif (digit == 33):	 #                           Apollo 13 explosion
				if (offBit):
					serialFromArduino.write(b'0,4,4,3,0\n')
					sleep(0.1)
					serialFromArduino.write(b'2,9,0,0,0\n')
					sleep(0.1)
					serialFromArduino.write(b'2,9,6,0,0\n')
					#sleep(0.1)
					#serialFromArduino.write(b'0,4,4,1,0\n') # Ox flow high
					sleep(0.1)
					serialFromArduino.write(b'0,4,4,2,2\n')	# Main Bus B Undervolt
				else:
					thirteen = True
#					serialFromArduino.write(b'0,4,4,3,0\n')

			elif (digit == 34):
				if (offBit):
					serialFromArduino.write(b'0,4,4,3,1\n')
					fan.fadeout(1000)
				else:
					serialFromArduino.write(b'1,4,4,3,1\n')
					offbit = 0
					fan.play()
			elif (digit == 35):
				if (offBit):
					serialFromArduino.write(b'0,4,4,3,2\n')
					fpump.fadeout(1000)
				else:
					serialFromArduino.write(b'1,4,4,3,2\n')
					offbit = 0
					fpump.play()
			elif (digit == 36):
				if (offBit):
					serialFromArduino.write(b'0,4,4,3,3\n')
					heat.fadeout(500)
				else:
					serialFromArduino.write(b'1,4,4,3,3\n')
					offbit = 0
					heat.play()
			elif (digit == 17):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					tei.play()	
					serialFromArduino.write(b'1,4,4,2,5\n')
					sleep(0.1)
					teiPushed = teiPushed + 1
					if teiPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,3\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 16):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					sps.play()	
					serialFromArduino.write(b'1,4,4,2,5\n')
					sleep(0.1)
					spsPushed = spsPushed + 1
					if (spsPushed % 10) == 0:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,4\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
					if spsPushed == 5:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,2\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
					if spsPushed == 25:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,3\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 31):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					miii.play()	 
					serialFromArduino.write(b'1,4,4,2,5\n')
					sleep(0.1)
					miiiPushed = miiiPushed + 1
					if miiiPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,1,3\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)

			elif (digit == 21):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					sivb.play()	 
					serialFromArduino.write(b'1,4,4,2,5\n')
					sivbPushed = sivbPushed + 1
					if sivbPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,1\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 20):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					sii.play()	
					serialFromArduino.write(b'1,4,4,2,5\n')
					siiPushed = siiPushed + 1
					if siiPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,0\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 19):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					sic.play()	
					serialFromArduino.write(b'1,4,4,2,5\n')
					sicPushed = sicPushed + 1
					if sicPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,1,3\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 22):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					mi.play()  
					serialFromArduino.write(b'1,4,4,2,5\n')
					miPushed = miPushed + 1
					if miPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,2\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 23):
				if (offBit): 
					offBit = 0
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					mii.play()	
					serialFromArduino.write(b'1,4,4,2,5\n')
					miiPushed = miiPushed + 1
					if miiPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,4\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 18):
				if (offBit):
					offBit = 0 
					serialFromArduino.write(b'0,4,4,2,5\n')
				else:
					tli.play()
					serialFromArduino.write(b'1,4,4,2,5\n')
					tliPushed = tliPushed + 1
					if tliPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,3\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 15):
				if (offBit):
					serialFromArduino.write(b'1,4,4,0,6\n')
					offbit = 0
					abortArmed = 1
				else:
					serialFromArduino.write(b'0,4,4,0,6\n')
					abortArmed = 0
			elif (digit == 9):
				if (offBit):
					serialFromArduino.write(b'0,4,4,2,6\n')
					flush.fadeout(2000)
				else:
					serialFromArduino.write(b'1,4,4,2,6\n')
					offbit = 0
					flush.play()
			elif (digit == 32):
				if (offBit):
					serialFromArduino.write(b'0,4,4,3,4\n')
					offBit = 0
					qout.play()
				else:
					serialFromArduino.write(b'1,4,4,3,4\n')
					qin.play()
			elif (digit == 2):
				if (offBit):
					serialFromArduino.write(b'0,4,4,2,7\n')
					aircomp.fadeout(2000)
					offBit = 0
				else:
					serialFromArduino.write(b'1,4,4,2,7\n')
					aircomp.play()
					suitCompPushed = suitCompPushed + 1
					sleep(0.1)
					if (suitCompPushed % 5) == 0:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,2,0\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 1):
				if (offBit):
					offbit = 0
					serialFromArduino.write(b'3,4,4,6,0\n')
				else:
					serialFromArduino.write(b'4,4,4,6,0\n')
			elif (digit == 10):
				if (offBit):
					serialFromArduino.write(b'0,4,4,1,7\n')
					sceAux = False
				else:
					offbit = 0
					serialFromArduino.write(b'1,4,4,1,7\n')
					sceAux = True
					if lightningStruck:
						sceRestored = True
			elif (digit == 11):
				if (offBit):
					serialFromArduino.write(b'0,4,4,1,6\n')
					dieselpump.fadeout(1000)
				else:
					serialFromArduino.write(b'1,4,4,1,6\n')
					offbit = 0
					dieselpump.play()
					glycolPushed = glycolPushed + 1
					if glycolPushed == 6:
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,0,0\n')
						sleep(0.1)
						serialFromArduino.write(b'1,4,4,3,6\n')
						cwsC.play(cws)
			elif (digit == 13):
				if (offBit):
					serialFromArduino.write(b'0,4,4,0,7\n')
					retract.stop()
					offBit = 0
				else:
					serialFromArduino.write(b'1,4,4,0,7\n')
					retract.play()
			elif (digit == 12):
				if (offBit):
					serialFromArduino.write(b'0,4,4,0,7\n')
					extend.stop()
					offBit = 0
				else:
					serialFromArduino.write(b'1,4,4,0,7\n')
					extend.play()
			elif (digit == 8):
				if (offBit):   
					serialFromArduino.write(b'0,4,4,3,5\n')
					cfan.fadeout(2000)
					offBit = 0
				else:
					serialFromArduino.write(b'1,4,4,3,5\n')
					cfan.play()
			elif (digit == 0):
				if (offBit):
					serialFromArduino.write(b'0,4,4,3,7\n')
					hflow.fadeout(500)
					offBit = 0
				else:
					serialFromArduino.write(b'1,4,4,3,7\n')
					hflow.play()
			
			sleep(0.01)
		except KeyboardInterrupt:
			exit()


thread1 = threading.Thread(target = mainLoop)
thread2 = threading.Thread(target = lightningStrike)
thread3 = threading.Thread(target = sceRestore)
thread13 = threading.Thread(target = thirteenEvent)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread13.start()
print "Exiting Main Thread"
