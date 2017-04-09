
# This program is based on the code and instructions from **SILVINO J. A. PRESA:
# <http://www.silvinopresa.com/how-to/python/control-a-servo-with-arduino-and-python-vpython/

# modified by bert@temminck.net

import OSC                                  # TODO check: https://github.com/ptone/pyosc
from   OSC import OSCServer, OSCClient
import serial
from   visual import *
import numpy as np
import sys
import socket


def get_Conrol():
    UDPserver = (serverAdr, serverPort)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(UDPserver)
    msgRaw, address = sock.recvfrom(200)
    n = msgRaw.find(chr(0))
    control = msgRaw[0:n]
    sock.close()
    return control

def servo_call(path, tags, args, source):
    msg_rotary1 = OSC.OSCMessage(rotary1)

    if path == rotary1:
        inData = float(args[0])
    if path == push1:
        inData = 0.0
        msg_rotary1.insert(0, inData)
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

    pos = int(180 * inData)  # map 0..1 -> 0..180 degrees
    servo_msg = chr(pos)  # convert integer -> ascii = chr(num), ascii -> integer = ord(num)
    print "%s => %.2f  %s" % (path, inData, str(pos))
    myLabel = 'angle: ' + str(pos)  # update the text of the label for the virtual environment
    data.write(servo_msg)  # code and send the angle to the Arduino through serial port
    angleLabel.text = myLabel  # refresh label on virtual environment
    #  calculate the new axis of the indicator
    measuringArrow.axis = (-10 * np.cos(pos * 0.01745), 10 * np.sin(pos * 0.01745), 0)
    msgStr = "angel: " + str(pos)
    msg_label1 = OSC.OSCMessage(label1)
    msg_label1.insert(0, msgStr)
    client.send(msg_label1)
    msg_led1 = OSC.OSCMessage(led1)
    msg_led1.insert(0, inData)
    client.send(msg_led1)

# Initalize ------------------------------------------------------------------------------------------------------------
fader1 = "/1/fader1"
rotary1 = "/1/rotary1"
label1 = "/1/label1"
led1 = "/1/led1"
push1 = "/1/push1"
push2 = "/1/push2"
push3 = "/1/push3"
push4 = "/1/push4"
push5 = "/1/push5"

serialPort = '/dev/tty.wchusbserialfa130'
serverAdr = "192.168.0.104"
serverPort = 8000
clientAdr = "192.168.0.102"
clientPort = 9000
data = serial.Serial(serialPort, 9600, timeout=1)

print >> sys.stderr, '\nArduino Uno Serial Port: %s ' % serialPort
print >> sys.stderr, '\n  iMac server: %s  port: %s' % (serverAdr, serverPort)
print >> sys.stderr, 'iPhone client: %s  port: %s' % (clientAdr, clientPort)
print >> sys.stderr, '\n waiting for client...'

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
    Conrol = get_Conrol()
    server = OSCServer((serverAdr, serverPort))  # iMac
    client = OSCClient()
    client.connect((clientAdr, clientPort))  # iPhone
    server.addMsgHandler(Conrol, servo_call)
    server.handle_request()
    rate(20)  # refresh rate required for VPython
    server.close()




