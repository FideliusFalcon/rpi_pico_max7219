# Raspberry Pico MAX7219 Matrix LED
An Pico integration to [mcauser' MicroPython MAX7219 libary](https://github.com/mcauser/micropython-max7219). This script has a method to make the text scroll inspired from [Alan Wang](https://www.hackster.io/alankrantas/simple-covid-19-cases-live-update-display-micropython-4607f2)

Le présent dépòt vous permet de faire défiler du texte sur un module MAX7219 à partir d'un Raspberry PICO (1ère génération).


## Wiring / Connexions
The Pico does'nt have a 5v pin, but the VBUS is connected to the power input. The MAX7219 need an 5v input, so the Pico's power supply will have to be 5v. This is the default pins for SPI0.

Le micro-contrôleur PICO n'offre pas de sortie 5V, mais la broche VBUS étant connectée au bus, nous pouvons utiliser cette source.
Le module MAX7219 nécessite 5V, vous les lui fournirez en exploitant la broche 40 (VBUS) comme suit: 

|MAX7219|Pico Name|Pico GPIO|Pico PIN|
|-|-|-|-|
|VCC|VBUS||40|
|GND|GND||38|
|DIN|MOSI (SPI0 TX)|GP7|10|
|CS|SPI0 CSn|GP5|7|
|CLK|SCK|GP6|9|

If you change the SPI clock pin (CS) remember to change it in code. 

N'oubliez pas de modifier votre code si vous changez de broche où connecter SPI (CS).
