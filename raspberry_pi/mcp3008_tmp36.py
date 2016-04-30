#!/usr/bin/python

""" 
    Code made with <3 by Julien Romero
    github.com/Aunsiels
"""

import spidev
import time
import os
import RPi.GPIO as GPIO
import smtplib
from enum import Enum
from email.mime.text import MIMEText


StateForce = Enum(
    "init",
    'read_full',
    'read_empty',
    'full',
    'near_empty',
    'empty')

def init_spi():
    """ init_spi Initializes the spi connection"""
    spi = spidev.SpiDev()
    spi.open(0,0)
    return spi

class ForceSensor:
    """"Force Sensor Represents a force sensor"""

    def __init__(self, channel, spi, name, button_full, button_empty):
        """ __init__ Initializes a force sensor

        :param channel : The channel number
        :param spi : The spi yhere to read
        :param name Name of the sensor
        :param button_full Pin number for calibration full
        :param button_empty Pin number for calibration empty
        """
        self.channel = channel
        self.full_value = -1
        self.empty_value = -1
	self.spi = spi
        self.state = StateForce.init
        self.name = name
        self.button_full = button_full
        self.button_empty = button_empty
        GPIO.setup(self.button_empty, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.button_full, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def read(self):
        """read reads the force sensor value, raw from ADC"""        
        adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def convert_volts(self, data, precision):
        """convert_volt Converts read data to volts
        
        :param data : the data to convert
        :param precision : The precision of the conversion
        """
        volts = (data * 3.3) / float(1023)
        volts = round(volts, precision)  
        return volts

    def read_empty(self):
        """read_empty Reads when the force sensor has an empty reserve"""
        self.empty_value = self.read()
        if self.state == StateForce.read_full:
            self.state = StateForce.full
        elif self.state == StateForce.init:
            self.state = StateForce.read_empty

    def read_full(self):
        """read_full Reads when the force sensor has a full reserve"""
        self.full_value = self.read()
        if self.state == StateForce.read_empty or self.state == StateForce.near_empty or self.state == StateForce.near_empty:
            self.state = StateForce.full
        elif self.state == StateForce.init:
            self.state = StateForce.read_full

    def get_percentage(self, precision):
        """get_percentage Get the current percentage
        
        :param precision : The precision of the conversion
        """
        diff = self.full_value - self.empty_value
        if diff != 0:
            res = (self.read() - self.empty_value) / float(diff)
            res = round(res, precision) 
         
            #State change
            if res >= -0.2 and res < 0.2:
                if res < 0.05:
                    if self.state == StateForce.near_empty or self.state == StateForce.full:
                        self.state = StateForce.empty
                        self.send_email("Empty", self.name + " empty.")
                elif  self.state == StateForce.full:
                        self.state = StateForce.near_empty
                        self.send_email("Near empty", self.name + " near empty.")
            elif res > 0.4 and (self.state == StateForce.near_empty or self.state == StateForce.empty):
                self.state = StateForce.full

            return res
        else:
            return -1

    def send_email(self, subject, msg):
        """send_email Sends an email to signal important events"""
        sender = '###'
        
        password = '###'
        
        receivers = ['forcesensorraspberry@gmail.com']
        
        message = MIMEText(msg)
        
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receivers[0]


        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(sender, password) 
        server.sendmail(sender, receivers, message.as_string())
        server.quit()

    def action(self):
        """"action Read the sensor and perform the good actions"""
        #First check if ye are trying to calibrate
        if GPIO.input(self.button_empty) == 0:
            self.read_empty()
        elif GPIO.input(self.button_full) == 0:
            self.read_full()
        else :
            percentage = self.get_percentage(2)
            # Print useful information
            print('Name :', self.name)
            print('Current percentage', percentage)
            print('Max value ', self.full_value) 
            print('Min value ', self.empty_value)
            print('Current state', self.state)


# Define delay between readings
delay = 1

#Initialize SPI
spi = init_spi()

#Initialize GPIO, to do before using sensors
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#Declare sensors
sensors =[ForceSensor(0, spi, "Sensor 1", 21, 20)]

while True:

    for s in sensors:
        s.action()

    # Wait before repeating loop
    time.sleep(delay)
 
