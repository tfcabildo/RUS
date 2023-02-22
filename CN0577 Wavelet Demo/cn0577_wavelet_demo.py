# Copyright (C) 2022 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# AUTHOR: TRISHA CABILDO

import os
import sys
import time
import math
import numpy as np
from adi import ltc2387
from wavelet_gen import random_ricker, wavdiff_out, wav_init, wav_close, wav_gen_main
from scipy.signal import cwt

n_samples = 256000                                                                              #Number of samples taken
sampling_freq = 10000000                                                                        #Master clock @120 MHz (f_sampling = master_clock / 12)
vref = 4.096                                                                                    #From REFBUF pin of LTC2387

#This function sets up the ADC
def setup_adc(my_ip):
    my_adc = ltc2387(uri=my_ip)
    my_adc.rx_buffer_size = n_samples
    my_adc.sampling_frequency = sampling_freq

    return my_adc

def adc_capture(my_adc):
    adc_data = my_adc.rx()
    time.sleep(2)

    return adc_data

def main():
    my_adc = setup_adc()
    m2k_ctx = wav_gen_main()
    adc_data = adc_capture()

    return m2k_ctx

if __name__ == '__main__':
    print("ADI packages import done")
    hardcoded_ip = 'ip:localhost'
    my_ip = sys.argv[2] if len(sys.argv) >= 3 else hardcoded_ip
    print("\nConnecting with CN0577 context at %s" % (my_ip))

    m2k_ctx = main()
    wav_close(m2k_ctx)