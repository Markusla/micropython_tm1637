# micropython_tm1637

Als Anfang habe ich die Pythonclasse von sd582 (http://www.forum-raspberrypi.de/Thread-led-4-segment-i2c-display?pid=137411#pid137411) für den Raspberry Pi 
umgeschrieben damit diese für MicroPython funktioniert.

Geplant ist es den Code noch etwas zu erweitern und zu verschönern.

Beispiel:
```
>>> import tm1637
>>> displ = tm1637.tm1637(16,14,2) # angeschlossen an ESP Pins 16 (CLK) und 14 (DIO)
>>> displ.Show([1,2,3,4]) # zweigt auf dem display 1234 an
```
