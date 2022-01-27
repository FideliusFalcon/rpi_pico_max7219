from sys import platform
import time
import gc
from machine import Pin, freq
from print_error import print_error  # Optional print of error codes
# Import all implemented classes
from nec import NEC_8, NEC_16
from sony import SONY_12, SONY_15, SONY_20
from philips import RC5_IR, RC6_M0
from mce import MCE

# Define pin according to platform
p = Pin(15, Pin.IN)
proto = 0

class show():
    IRred = ""
    IRtxt = ""
    CUMUL = "swich={"
    FINAL = "show.TXT = switch.get(val, \"Rien\")"

    def __init__(self):
        self.LECTURE = ""

# User callback
def cb(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        print('Data {:02x} Addr {:04x} Ctrl {:02x}'.format(data, addr, ctrl))
        val = str('{:02x}'.format(data))
        txt.CUMUL = txt.CUMUL + "'{:02x}': ''".format(str(val), txt.IRtxt)
            
classes = (NEC_8, NEC_16, SONY_12, SONY_15, SONY_20, RC5_IR, RC6_M0, MCE)
ir = classes[proto](p, cb)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information
txt = show()

# **** DISPLAY GREETING ****
s = '''Test for IR receiver.
We`ll test every single button of your remote.
First: brand and name of your remote
Second: ON/OFF button and numbers
Third: all other buttons you`ll want
       Let entry blank to finish

Hit ctrl-c to stop, then ctrl-d to soft reset... you`ll lose data'''
print(s)

brand = input("Your remote brand : ")
model = input("Your remote model : ")

txt.IRtxt = "POWER"
num = print("Please press POWER button ")
for t in range(0, 9999):
    gc.collect()
    time.sleep(3)
for x in range(0, 10):
    txt.IRtxt = str(x)
    num = print("Please press the number " + str(x))
    for t in range(0, 9999):
        gc.collect()
        time.sleep(3)

print("Voici la cueillette : " + txt.CUMUL)
#try:
#    while True:
#        # A real application would do something here...
#        print('running')
#        gc.collect()
#        time.sleep(5)
#except KeyboardInterrupt:
#    ir.close()
