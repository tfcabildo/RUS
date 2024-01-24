# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 08:57:44 2020

@author: tcabildo
"""

#This is a control code for the Chroma Supply.Code contains functions commonly used.

import pyvisa as visa
import time

rm = visa.ResourceManager()
print(rm.list_resources())

#Setting the instrument name
supply = rm.open_resource('USB0::0x1698::0x0837::005000001044::INSTR')

#Function to set supply ON
def ON_power ():
    supply.write('CONFigure:OUTPut ON')
    return None

#Function to set supply OFF
def OFF_power():
    supply.write('ABORt')
    return None

#Function to set output voltage and current
def set_out (v, c):
    voltage = "SOUR:VOLT " + str(v)
    curr = "SOUR:CURR " + str(c)
    supply.write(voltage)
    supply.write(curr)
    supply.write('SOUR:CURR:LIMIT:HIGH 2.5')
    return None

#Funtion to fetch supply measurements
def fetch_supply_out ():
    v = supply.query('FETC:VOLT?')
    c = supply.query('FETC:CURR?')
    p = supply.query('FETC:POW?')
    return v,c,p

set_out(12.0, 2.5)
ON_power()
time.sleep(2)
print(fetch_supply_out())
time.sleep(2)
OFF_power
