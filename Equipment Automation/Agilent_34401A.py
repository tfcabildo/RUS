# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 08:57:44 2020

@author: tcabildo
"""

#This is a control code for the Chroma Supply.Code contains functions commonly used.

import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())

#Setting the instrument name
meter = rm.open_resource('GPIB0::21::INSTR')

#Function to set supply ON
def ON_power ():
    meter.write('CONFigure:OUTPut ON')
    return None

#Function to set supply OFF
def OFF_power():
    meter.write('CONFigure:OUTPut OFF')
    return None

def set_remote():
    meter.write('SYSTem:REMote')
    print("Remote good!")
    return None

#Function to set supply OFF
def fetch_out():
    meter.query('MEASure:VOLTage:DC?')
    meter.query('MEASure:CURRent:DC?')
    return None

def beeper():
    meter.write('SYSTem:BEEPer')
    meter.write('SYSTem:BEEPer:STATe ON')

set_remote()
beeper()
OFF_power()
#print(dmm_id())
