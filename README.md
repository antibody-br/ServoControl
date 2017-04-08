 
![Blogo](images/LOGOs.png)

# ServoControl
## Remote control using Python, Arduino, OSC and TouchOSC App with Smartphone (iPhone iOS or Android)

This program is based on the code and instructions from **SILVINO J. A. PRESA**: <http://www.silvinopresa.com/how-to/python/control-a-servo-with-arduino-and-python-vpython/> **<-THANK YOU!** very, very much, it helped a lot.

I am not an experience Python programmer, so I wrote a mickey-mouse program to control a servo with my iPhone.
There are for sure much clever way's to do this, so all feedback and improvements are very welcome.

 
For instance I use an UDP server to get the controller path from the touchOSC app and then I start a OSC server to control it. There must be a smarter way to do this.

**so here we go:**

##Prerequisites:
###Software

* **Python editor:** I prefer PyCharm (mac/win): <https://www.jetbrains.com/pycharm/> 
* **Arduino IDE:** <https://www.arduino.cc/en/main/software>
* **touchOSC app:** iOS: <https://hexler.net/software/touchosc> android: <https://hexler.net/software/touchosc-android>  price: $5
* **touchOSC editor:** <https://hexler.net/software/touchosc> scroll nearly too the end of the page: Downloads -> choose your OS.

###Python Modules
I use  **Python 2.7.13**, on the **Mac** be sure you use the FrameWork version, otherwise the Vpython graphic display will not work: ```/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7```

* **OSC:** Unix terminal: ```$ pip install pyosc``` or download: <https://github.com/ptone/pyosc>
* **Vpython:**```$ pip install vpython```
* ***serial:***```$ pip install pyserial```
* ***numpy:***```$ pip install numpy```
* ***socket:*** I guess it is a standard Python package, but had a lot of trouble getting it working. Be sure you have no other socket.py some where in your directories.

###Arduino Libraries:
**Servo:** <https://www.arduino.cc/en/reference/servo>

###Hardware
* **Arduino Board (Uno):** <https://www.arduino.cc/> and many other companies. Mine comes from China (Oops!)
* **Servo Motor:** I use TowerPro SG90, do a google search and you get a lot of hits.
