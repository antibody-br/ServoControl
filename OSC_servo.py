
# This program is based on the code and instructions from SILVINO J. A. PRESA:
# <http://www.silvinopresa.com/how-to/python/control-a-servo-with-arduino-and-python-vpython/

# modified by -=b=- apr-2017: bert@temminck.net

import OSC                                 
from   OSC import OSCServer, OSCClient
import serial
from   visual import *
import numpy as np
import sys
import socket

def get_Conrol():                                                 # read from Phone touchOSC e.g "/1/rotary1"
    UDPserver = (serverAdr, serverPort)                           # define UDP server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # create a socket
    sock.bind(UDPserver)                                          # bind socket to server
    msgRaw, address = sock.recvfrom(50)                           # read received data to <msgRaw>, buffer 50 bits
    n = msgRaw.find(chr(0))                                       # find position of first assci char <0>
    control = msgRaw[0:n]                                         # cut out the string with the path e.g "/1/rotary1"
    sock.close()                                                  # close the socket
    return control                                                # and return this string

def servo_call(path, tags, args, source):                         # read incomming data from touchOSC
    msg_rotary1 = OSC.OSCMessage(rotary1)                         # and if nessary returns data too touchOSC

    if path == rotary1:                                           # if control is <rotary>, read a value between 0..1
        inData = float(args[0])                                   # from the phone
    if path == push1:                                             # if control is push button on the phone
        inData = 0.0                                              # set value, 0 = 0 degrees, 1 = 180 degrees
        msg_rotary1.insert(0, inData)                             # set on phone the rotary control in desired position
        client.send(msg_rotary1)
    if path == push2:
        inData = 0.25
        msg_rotary1.insert(0, inData)
        client.send(msg_rotary1)
    if path == push3:
        inData = 0.5
        msg_rotary1.insert(0, inData)
        client.send(msg_rotary1)
    if path == push4:
        inData = 0.75
        msg_rotary1.insert(0, inData)
        client.send(msg_rotary1)
    if path == push5:
        inData = 1.0
        msg_rotary1.insert(0, inData)
        client.send(msg_rotary1)

    pos = int(180 * inData)                                     # map 0..1 -> 0..180 degrees
    servo_msg = chr(pos)                                        # convert integer -> ascii = chr(num)
    print "%s => %.2f  %s" % (path, inData, str(pos))           # other way around:  ascii -> integer = ord(num)
    myLabel = 'angle: ' + str(pos)                              # update the text label for the virtual environment
    data.write(servo_msg)                                       # send the angle to the Arduino through serial port
    angleLabel.text = myLabel                                   # refresh label on virtual environment
    #  calculate the new axis of the indicator
    measuringArrow.axis = (-10 * np.cos(pos * 0.01745), 10 * np.sin(pos * 0.01745), 0)
    msgStr = "angel: " + str(pos)
    msg_label1 = OSC.OSCMessage(label1)                         # define angle label on touchOSC phone
    msg_label1.insert(0, msgStr)                                # make string out of it
    client.send(msg_label1)                                     # send string to touchOSC phone
    msg_led1 = OSC.OSCMessage(led1)                             # define LED in middle of rotary
    msg_led1.insert(0, inData)                                  # make the led string 0 = off, 1 = full red
    client.send(msg_led1)                                       # and send the string to touchOSC phone

# Initalize ------------------------------------------------------------------------------------------------------------
# define the different controlls on touchOSC, you see them in the touchOSC Editor if you create a new controll
# be carfull, if you delete a control in the touchOSC Editor, and create a new one, it will be e.g. "/1/fader2"
fader1 = "/1/fader1"
rotary1 = "/1/rotary1"
label1 = "/1/label1"
led1 = "/1/led1"
push1 = "/1/push1"
push2 = "/1/push2"
push3 = "/1/push3"
push4 = "/1/push4"
push5 = "/1/push5"

# serialPort on the Mac it is something like this, on WIN is something like: COMn
# in the Arduino IDE on your computer you can see the serial port name in the menubar -> Tools -> port
serialPort = '/dev/tty.wchusbserialfa130'
serverAdr = "192.168.0.104"                                     # ip address of your computer
serverPort = 8000                                               # port number used on your computer
clientAdr = "192.168.0.103"                                     # ip address of your phone, find it on touchOSC
clientPort = 9000                                               # port number of touchOSC on your phone
data = serial.Serial(serialPort, 9600, timeout=1)               # data send to Arduino via serial port (UBS connetion)
''' 
WARNING: if you not use a fix IP address, but get if from a DHCP server, the IP address can change
special on the Phone, that is reconecting to your network if you return from an other place.
error message is: 
OSCServer: NoCallbackError on request from 192.168.0.103:64550: No callback registered to handle OSC-address '/1/push2'
you see: if have my Phone <clientAdr> defined as "192.168.0.102" but it is now: "192.168.0.103'
'''

print >> sys.stderr, '\nArduino Serial Port: %s ' % serialPort
print >> sys.stderr, '    Computer server: %s  port: %s' % (serverAdr, serverPort)
print >> sys.stderr, '       Phone client: %s  port: %s' % (clientAdr, clientPort)
print >> sys.stderr, '\n waiting for Phone...'

# Create virtual environment -------------------------------------------------------------------------------------------
# first we create the arrow to show current position of the servo
measuringArrow = arrow(pos=(0, -10, 0), axis=(0, 10, 0), shaftwidth=0.4, headwidth=0.6)
# and now the labels
angleLabel = label(text='angle: 90', pos=(0, 5, 0), height=15, box=false)
angle0 = label(text='0', pos=(-10, -10, 0), height=15, box=false)
angle45 = label(text='45', pos=(-7.5, -2.5, 0), height=15, box=false)
angle90 = label(text='90', pos=(0, 1, 0), height=15, box=false)
angle135 = label(text='135', pos=(7.5, -2.5, 0), height=15, box=false)
angle180 = label(text='180', pos=(10, -10, 0), height=15, box=false)

# Main -----------------------------------------------------------------------------------------------------------------

while True:
    Conrol = get_Conrol()                                   # get path control string from Phone touchOSC
    server = OSCServer((serverAdr, serverPort))             # define OSC server on computer
    client = OSCClient()                                    # define OSC client on Phone touchOSC
    client.connect((clientAdr, clientPort))                 # connect to client           
    server.addMsgHandler(Conrol, servo_call)                # use the control path and process message
    server.handle_request()                                 # handle request
    rate(20)                                                # refresh rate required for VPython
    server.close()                                          # close the server, start over again and again.




