#!/usr/bin/env python

import os
from os import system
import curses
import glob
import time 
import RPi.GPIO as GPIO

svar = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT) 
GPIO.setup(18, GPIO.OUT) 

while svar != ord('4'):
     screen = curses.initscr()

     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Welcome to your coffee maker")
     screen.addstr(4, 4, "1 - Turn on coffeepot")
     screen.addstr(5, 4, "2 - Check sensor information")
     screen.addstr(6, 4, "3 - Make tea")
     screen.addstr(7, 4, "4 - End program")
     screen.refresh()

     svar = screen.getch()

     if svar == ord('1'):
        GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18,GPIO.LOW)
     if svar == ord('2'):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        def read_temp_raw():
            f = open(device_file, 'r')
       	    lines = f.readlines()
            f.close()
            return lines
        def read_temp():
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
       	        temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c #add temp_f for fahrenheit
        timeout = time.time() + 5 
        while True:
         if time.time() > timeout:
           break
         screen.clear()
         screen.addstr(4, 6, str(int(read_temp())) + "C" ) 
         screen.refresh()
        
     if  svar == ord('3'):
          curses.endwin()
          screen.clear()
          screen.addstr(4, 6, "This is not a teapot")
          screen.refresh()
          time.sleep(5) 

curses.endwin()


