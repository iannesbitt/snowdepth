#!/usr/bin/python
# Filename: maxSonarTTY.py

# Reads serial data from Maxbotix ultrasonic rangefinders
# Gracefully handles most common serial data glitches
# Use as an importable module with "import MaxSonarTTY"
# Returns an integer value representing distance to target in millimeters

from time import time, sleep
from datetime import datetime
import pytz
from serial import Serial
import pigpio

serialDevice = "/dev/ttyAMA0" # default for RaspberryPi
maxwait = 5 # seconds to try for a good reading before quitting
now = datetime.now(pytz.timezone('America/Denver')).strftime('%Y-%m-%d %H:%M:%S')
on_pin = 22

def measure(portName):
    ser = Serial(portName, 9600, 8, 'N', 1, timeout=3)
    timeStart = time()
    valueCount = 0

    while time() < timeStart + maxwait:
        if ser.inWaiting():
            bytesToRead = ser.inWaiting()
            valueCount += 1
            if valueCount < 2: # 1st reading may be partial number; throw it out
                continue
            testData = ser.read(bytesToRead)
            if not testData.startswith(b'R'):
                # data received did not start with R
                continue
            try:
                sensorData = testData.decode('utf-8').lstrip('R')
            except UnicodeDecodeError:
                # data received could not be decoded properly
                continue
            try:
                mm = int(sensorData)
            except ValueError:
                # value is not a number
                continue
            ser.close()
            return(mm)

    ser.close()
    raise RuntimeError("Expected serial data not received")


if __name__ == '__main__':
    pi = pigpio.pi()
    pi.write(on_pin, 1) # turn on sonar
    sleep(2) # wait 2 seconds for sonar to power up

    measurement = measure(serialDevice)

    pi.write(on_pin, 0) # turn off sonar
    sleep(2)
    pi.stop()

    #print("distance =",measurement)
    print("%s,%s" % (now,measurement))
