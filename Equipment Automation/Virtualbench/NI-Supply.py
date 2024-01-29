#! /usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2024 Trisha Cabildo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, DmmFunction
import time

device_name = 'VB8012-32C3456'

# Replace "myVirtualBench" with the name of your device. The device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
# Check the device's name in the VirtualBench Application under File->About
def VB_setup():
    virtualbench = PyVirtualBench(device_name)
    return virtualbench

def set_DC_out(my_supply,chx, v, c):
    my_supply.configure_voltage_output(chx,v,c)
    my_supply.enable_all_outputs(True)
    time.sleep(2)
    return

def print_DC_out(my_supply,chx):
    voltage_measurement, current_measurement, ps_state = my_supply.read_output(chx)
    print("Measurement: %f V\t%f A\t(%s)" % (voltage_measurement, current_measurement, str(ps_state)))
    return

def main():
    try:
        # Power Supply Configuration
        channel = "ps/+25V"
        voltage_level = 20.0
        current_limit = 0.5

        virtualbench = VB_setup()
        ps = virtualbench.acquire_power_supply()
        dmm = virtualbench.acquire_digital_multimeter()

        set_DC_out(ps,channel,voltage_level,current_limit)
        print_DC_out(ps,channel)
        set_DC_out(ps,channel,0,0.005)
        print_DC_out(ps,channel)
        
        ps.release()
    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        virtualbench.release()

if __name__ == '__main__':
    main()
