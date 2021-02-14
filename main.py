import max7219
from machine import Pin, SPI
from time import sleep

class matrix():
    def __init__(self):
        self.MAX7219_NUM = 4
        self.MAX7219_INVERT = False
        self.MAX7219_SCROLL_DELAY = 0.03
        cs_pin = 5

        spi = SPI(0)
        self.display = max7219.Matrix8x8(spi=spi, cs=Pin(cs_pin), num=self.MAX7219_NUM)
        self.display.brightness(2)
    
    def text_scroll(self, text, scroll_delay=None):
        if scroll_delay != None:
            self.MAX7219_SCROLL_DELAY = scroll_delay
        
        p = self.MAX7219_NUM * 8
        for p in range(self.MAX7219_NUM * 8, len(text) * -8 - 1, -1):
            self.display.fill(self.MAX7219_INVERT)
            self.display.text(text, p, 1, not self.MAX7219_INVERT)
            self.display.show()
            sleep(self.MAX7219_SCROLL_DELAY)

led = matrix()
text = "HELLO REDDIT FROM RASPBERRY PICO"
led.text_scroll(text)

