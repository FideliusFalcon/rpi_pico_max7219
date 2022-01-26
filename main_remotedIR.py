from sys import platform
import max7219
from machine import Pin, SPI, freq
from time import sleep
import gc
from print_error import print_error  # Optional print of error codes
# Import all implemented classes
from nec import NEC_8, NEC_16
from sony import SONY_12, SONY_15, SONY_20
from philips import RC5_IR, RC6_M0
from mce import MCE

# Define pin according to platform
p = Pin(15, Pin.IN)


class matrix():
    bright = 9
    invert = False
    LECTURE = ""
    VISIBLE = "Ceci"
    MAX7219_NUM = 1
    MAX7219_INVERT = invert
    MAX7219_SCROLL_DELAY = 0.15
#   MAX7219_SCROLL_DELAY = 0

    def __init__(self):
        cs_pin = 5
        spi = SPI(0)
        self.display = max7219.Matrix8x8(spi=spi, cs=Pin(cs_pin), num=self.MAX7219_NUM)
        self.display.brightness(self.bright)
    
    def text_scroll(self):
        p = self.MAX7219_NUM * 8
        for p in range(self.MAX7219_NUM * 8, len(self.VISIBLE) * -8 - 1, -1):
            self.display.fill(self.MAX7219_INVERT)
            self.display.text(self.VISIBLE, p, 1, not self.MAX7219_INVERT)
            self.display.show()
            sleep(self.MAX7219_SCROLL_DELAY)
    def text_fixe(self):
        self.display.fill(self.MAX7219_INVERT)
        self.display.text(self.VISIBLE, 0, 1, not self.MAX7219_INVERT)
        self.display.show()
    def affiche(self):
        if self.MAX7219_SCROLL_DELAY == 0:
            self.text_fixe()
        else:
            self.text_scroll()
    def ir_rcv(self, data):
        if data == "FIN":
            data = ""
            self.VISIBLE = self.LECTURE
            self.LECTURE = ""
        if data == "Defilement":                    #Touche "Pause"
            self.LECTURE = ""
            if self.MAX7219_SCROLL_DELAY == 0:
                self.MAX7219_SCROLL_DELAY = 0.15
            else:
                self.MAX7219_SCROLL_DELAY = 0
        if data == "+":                             #Touche "+"
            self.LECTURE = ""
            self.MAX7219_SCROLL_DELAY = self.MAX7219_SCROLL_DELAY * 0.8
        if data == "-":                             #Touche "-"
            self.LECTURE = ""
            self.MAX7219_SCROLL_DELAY = self.MAX7219_SCROLL_DELAY * 1.25
        if data == "OFF":
            if self.bright == 0:
                self.bright = 9
            else:
                self.bright = 0
            self.display.brightness(self.bright)
        if data == "USB":                             #Touche "USB"
            if self.invert == True:
                self.invert = False
            else:
                self.invert = True
            self.MAX7219_INVERT = self.invert
        else:
            self.LECTURE = self.LECTURE + data
        data = ""

# User callback
def cb(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        val = str('{:02x}'.format(data))
        switch={
            '16':'0',
            '0c':'1',
            '18':'2',
            '5e':'3',
            '08':'4',
            '1c':'5',
            '5a':'6',
            '42':'7',
            '52':'8',
            '4a':'9',
            '19':'FIN',        #button 'twisted arrows' used as "Enter" to apply the changes and display new text
            '0d':'USB',        #button 'USB' used for swap between inverse video and normal
            '07':'Allo!',      #button 'EQ'
            '15':'-',          #button - used to decelerate the scrolling
            '09':'+',          #button + used to accelerate the scrolling
            '44':'Pause',      #button 'pause'
            '40':'Recule',     #button 'Ffoward'
            '43':'Avance',     #button 'Fback'
            '45':'OFF',        #button ON/OFF used to turn the panel OFF  (to swap brightness between 0 and 9)
            '46':'Defilement', #buttun Mode used to swap between scrolling and static text
            '47':'Sourdine'    #button MUTE
            }
        led.ir_rcv(switch.get(val, "Rien"))

#Objects definitions
led = matrix()
classes = (NEC_8, NEC_16, SONY_12, SONY_15, SONY_20, RC5_IR, RC6_M0, MCE)
ir = classes[0](p, cb)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

try:
    while True:
        gc.collect()
        led.affiche()
#        if valeurLue != "Rien" and valeurLue != None:
#            print(valeurLue)
except KeyboardInterrupt:
    ir.close()
    print("Fin du test")

