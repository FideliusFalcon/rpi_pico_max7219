# Raspberry Pico MAX7219 Matrix LED
An Pico integration to [mcauser' MicroPython MAX7219 libary](https://github.com/mcauser/micropython-max7219). 
This script has a method to make the text scroll inspired from [Alan Wang](https://www.hackster.io/alankrantas/simple-covid-19-cases-live-update-display-micropython-4607f2)
This script permits to change the text shown on the Matrix LED usign a IR remote control.

Le présent dépòt vous permet de faire défiler du texte sur un module MAX7219 à partir d'un Raspberry PICO (1ère génération).
Ce script permet de modifier le texte affiché sur la matrice 8x8 (DEL) à l'aide d'une télécommande à infra-rouges.


## Wiring / Connexions
The Pico does'nt have a 5v pin, but the VBUS is connected to the power input. The MAX7219 need an 5v input, so the Pico's power supply will have to be 5v. This is the default pins for SPI0.

Le micro-contrôleur PICO n'offre pas de sortie 5V, mais la broche VBUS étant connectée au bus, nous pouvons utiliser cette source.
Les modules MAX7219 (qui nécessite 5V, vous les lui fournirez en exploitant la broche 40 (VBUS)) et lecteur infra-rouge comme suit: 

|MAX7219|Pico Name|Pico GPIO|Pico PIN|IR reader|
|-|-|-|-|-|
|GND|GND||3|-|
|CS|SPI0 CSn|GP5|7|-|
|CLK|SCK|GP6|9|-|
|DIN|MOSI (SPI0 TX)|GP7|10|-|
|-|SP1TX|GP15|20|S(ignal)|
|-|VCC|3.3 V|36|VCC|
|-|GND||38|GND|
|VCC|VBUS||40|-|

If you change the SPI clock pin (CS) remember to change it in code. 

N'oubliez pas de modifier votre code si vous changez de broche où connecter SPI (CS).

## Links / Liens
[framebuf --- documentation](http://docs.micropython.org/en/latest/pyboard/library/framebuf.html)


