# chilimonitor

Very simple implementation of temperature logger of chili plants using a raspberry pi.

Script is constantly running, every fifteen minutes:

* Get current temperature from sensor
* Add to deque collection (to keep a days worth)
* Create js to create graph
* Copy js to webserver

On server:

* Page which includes the js supplied by RPi

tempnow.py returns current time, used in images project
