import pygame    
import time
#import pygame.mixer
import serial 

serialFromArduino = serial.Serial("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1004cms-if00-port0", 115200)
#serialFromArduino = serial.Serial("/dev/ttyAMA0", 115200)
serialFromArduino.flush()


#VERY IMPORTANT THAT THESE NEXT TWO LINES OF MIXER INIT GO BEFORE PYGAME.INIT !!!!!!!
#OTHERWISE A VEXING DELAY OCCURS BEFORE MIXER COMMANDS ARE CARRIED OUT.
pygame.mixer.pre_init(48000, -16, 1, 1024) #was 1024
pygame.mixer.init()
#DON'T PUT PYGAME.INIT BEFORE MIXER.INIT!
pygame.init()

pygame.mixer.set_num_channels(14)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

blaster1 = pygame.mixer.Sound("/home/pi/space/blaster1.wav")
blaster2 = pygame.mixer.Sound("/home/pi/space/blaster2.wav")
blaster3 = pygame.mixer.Sound("/home/pi/space/blaster3.wav")
blaster4 = pygame.mixer.Sound("/home/pi/space/blaster4.wav")
alien1 = pygame.mixer.Sound("/home/pi/space/alien1.wav")
alien2 = pygame.mixer.Sound("/home/pi/space/alien2.wav")
alien3 = pygame.mixer.Sound("/home/pi/space/alien3.wav")
alien4 = pygame.mixer.Sound("/home/pi/space/alien4.wav")
ufo1 = pygame.mixer.Sound("/home/pi/space/ufo1.wav")
ufo2 = pygame.mixer.Sound("/home/pi/space/ufo2.wav")

sivb = pygame.mixer.Sound("/home/pi/space/sivb.wav")
mi = pygame.mixer.Sound("/home/pi/space/mi.wav")
mii = pygame.mixer.Sound("/home/pi/space/mii.wav")
loop = pygame.mixer.Sound("/home/pi/space/rocketloop.wav")

azeroC = pygame.mixer.Channel(1)
aoneC = pygame.mixer.Channel(2)
atwoC = pygame.mixer.Channel(3)
athreeC = pygame.mixer.Channel(4)

b1C = pygame.mixer.Channel(5)
b2C = pygame.mixer.Channel(6)
b3C = pygame.mixer.Channel(7)
b4C = pygame.mixer.Channel(8)
b5C = pygame.mixer.Channel(9)
b6C = pygame.mixer.Channel(10)
b7C = pygame.mixer.Channel(11)
b8C = pygame.mixer.Channel(12)

axeschannels = [azeroC, aoneC, atwoC, athreeC]
buttonchannels = [b1C, b2C, b3C, b4C, b5C, b6C, b7C, b8C]

axessounds = [mi, mi, mi, loop]
buttonsounds = [blaster1, blaster2, blaster3, blaster4, alien1, alien2, alien3, alien4, ufo1, ufo2]

buttonnumbers =[0,1,2,3,10,11,12,13,14]
axeszero = [0.0,0.0,0.0,0.0]
axesstate = [0.0,0.0,0.0,0.0]
mainValue = 0
topValue = 0
bottomValue = 0
leftValue = 0
rightValue = 0
axesvalue = [topValue,bottomValue,leftValue,rightValue]
lastCommand = ''
timeLastCommand = time.time()

# Get count of joysticks
joystick_count = pygame.joystick.get_count()

joystick = pygame.joystick.Joystick(0)
joystick.init()

axes = joystick.get_numaxes()

#for i in range(axes):
#    axeschannels[i] = axessounds[i].play(-1)

#athreeC = loop.play(-1)

def zeroAxes():
    axes = joystick.get_numaxes()
    for i in range( axes ):
        axis = joystick.get_axis( i )
        #print("Axis {} value: {:>6.3f}".format(i, axis) )
        axeszero[i] = axis
    
mainEngineOn = False

# -------- Main Program Loop -----------
while True:
    # EVENT PROCESSING STEP
#    pygame.event.pump()
    for event in pygame.event.get(): # User did something
        #if event.type == pygame.QUIT: # If user clicked close
            #done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            if (joystick.get_button(9) == 1):
                zeroAxes()
            if (joystick.get_button(10) == 1):
                subprocess.call(['mpg123 /home/pi/space/aborted.mp3'], shell=True)
                subprocess.call(['shutdown -h now "System halted by joystick button"'], shell=True)
            buttons = joystick.get_numbuttons()
            for i in range( 8 ):
               button = joystick.get_button( buttonnumbers[i] )
               if (button == 1):
                   buttonchannels[i].play(buttonsounds[i])
               #print("Button {:>2} value: {}".format(i,button) )
#        if event.type == pygame.JOYBUTTONUP:
#            print("Joystick button released.")
        if event.type == pygame.JOYAXISMOTION:
            for i in range( 3 ):
                axis = joystick.get_axis( i )
                if abs(axis - axeszero[i]) > 0.06:
                    if (axeschannels[i].get_busy() == False):
                        axeschannels[i].play(axessounds[i])
                    axeschannels[i].set_volume((abs(axis - axeszero[i]) * 2.5 ) + 0.0)
                    if i == 0:
                        if (axis > axeszero[i]):
                            topValue = 0
                            bottomValue = (abs(axis - axeszero[i]) * 24.2)
                            #bottomValue = 9
                            #print bottomValue
                        elif (axis < axeszero[i]):
                            topValue = (abs(axis - axeszero[i]) * 12.5)
                            #topValue = 9
                            bottomValue = 0
                            #print topValue
                    elif i == 1:
                        if (axis > axeszero[i]):
                            leftValue = 0
                            rightValue = (abs(axis - axeszero[i]) * 26.1)
                            #print rightValue
                        elif (axis < axeszero[i]):
                            leftValue = (abs(axis - axeszero[i]) * 12.8378)
                            rightValue = 0
                            #print leftValue
                else:
                    axeschannels[i].fadeout(50)
                    if i == 0:
                        topValue = 0
                        bottomValue = 0
                    elif i == 1:
                        leftValue = 0
                        rightValue = 0
            i=3
            axis = joystick.get_axis( i )
            #serialFromArduino.write(b'(abs(axis - axesstate[i]) * 9),0,0,0,0\n')
            if abs(axis - axeszero[i]) > 0.03:
                mainValue = (abs(axis - axeszero[i]) * 7)
#                    commandString = "{},{},{},{},{}\n".format(mainValue,0,0,0,0)
#                    serialFromArduino.write((commandString))

                mainEngineOn = True
                if (axeschannels[i].get_busy() == False):
                    axeschannels[i].play(axessounds[i])
                axeschannels[i].set_volume((abs(axis - axeszero[i]) * 1 ) + 0.0)
                #serialFromArduino.write(b'(9,0,0,0,0\n')
                #serialFromArduino.write(b'(abs(axis - axesstate[i]) * 1),0,0,0,0\n')
            else:
                axeschannels[i].fadeout(50)
                mainValue = 0
                #if mainEngineOn is True:
                #    mainValue = 0
                    #serialFromArduino.write(b'0,0,0,0,0\n')
                #    mainEngineOn = False
            axesstate[i] = axis
            #mainValue = 9
#            commandString = "9,9,9,9,9\n"
#            serialFromArduino.write((commandString))
            commandString = "{:1.0f},{:1.0f},{:1.0f},{:1.0f},{:1.0f}\n".format(mainValue,topValue,bottomValue,leftValue,rightValue)
            #print commandString
            if commandString != lastCommand:
                print (time.time() - timeLastCommand)
                if time.time() - timeLastCommand > 0.05:
                    serialFromArduino.write((commandString))
                    timeLastCommand = time.time()
                            #time.sleep(0.05)
            lastCommand = commandString

    # Limit to 50 frames per second
    clock.tick(30)
    #time.sleep(1)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
