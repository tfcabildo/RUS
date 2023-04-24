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

import sys
import libm2k
import numpy as np
from scipy.signal import periodogram,find_peaks,ricker, resample
import matplotlib.pyplot as plt

#Samples per second
sr = 7500000                                                    # Sample rate
N = 750000                                                      # Number of samples
t = np.arange(0,1,1/N)
vcm = 2.048                                                     # VCM of LT2387 (2.048 V default)
l, h = 0, 0.005

available_sample_rates= [750, 7500, 75000, 750000, 7500000, 75000000]
max_rate = available_sample_rates[-1]                           # last sample rate = max rate
min_nr_of_points=10
max_buffer_size = 500000

def wav_init():
    ctx=libm2k.m2kOpen()
    if ctx is None:
        print("Connection Error: No ADALM2000 device available/connected to your PC.")
        sys.exit("m2k error")
    ctx.calibrateDAC()
    ctx.calibrateADC()
    return(ctx)

def wav_close(ctx):
    libm2k.contextClose(ctx)
    del ctx

def random_ricker():
    vpp = 0.5                                                    # Peak to peak amplitude of wavelet
    n_peak = 2                                                   # Number of wavelet peaks
    n_points = int(N/n_peak)                                     # Number of points per wavelet
    
    width_param = int(n_points * 0.05 * np.random.random())      # 5% width parameter; Randomizes the width of the wavelet                                             
    x = ricker(n_points, width_param * np.random.random())       # Generate wavelet
    v_scale = vpp/(np.max(x)-np.min(x))/2                        # Scale to fit vpp
    x = x * v_scale
    rick_offset = 0 - np.min(x)                             
    x = x + rick_offset

    if n_peak > 1:
        ricker_wav = np.concatenate((x,x))
        for _ in range(1,n_peak-1):
            ricker_wav= np.concatenate((ricker_wav,x))
    else:
        ricker_wav = x

    return x - np.average(x)

def ricker_gen():
    vpp =  0.5                              
    n_peak= 2                               
    n_points = int(N/n_peak)                
    width_param = int(n_points*.05)         
    vcm = 2.048                             
    x = ricker(n_points,width_param)        
    v_scale = vpp/(np.max(x)-np.min(x))/2   
    x = x*v_scale
    rick_offset = 0 - np.min(x)
    x = x + rick_offset

    if n_peak > 1:
        ricker_wav = np.concatenate((x,x))
        for _ in range(1,n_peak-1):
            ricker_wav= np.concatenate((ricker_wav,x))
    else:
        ricker_wav = x

    return ricker_wav

def wavsingle_out(ctx, ricker_wav):
    aout=ctx.getAnalogOut()
    aout.setSampleRate(0, sr)
    aout.setSampleRate(1, sr)
    aout.enableChannel(0, True)
    aout.enableChannel(1, True)
    w1_data = ricker_wav
    w2_data = ricker_wav

    buffer1 = w1_data
    buffer2 = w2_data
    buffer = [buffer1, buffer2]

    m2k_out = np.asarray(buffer1)
    m2k_out = m2k_out.reshape(N,1)

    aout.setCyclic(True)
    aout.push(buffer)
    print("Wavelet Generated")

def wavdiff_out(ctx):
    aout = ctx.getAnalogOut()
    aout.setSampleRate(0, sr)
    aout.setSampleRate(1, sr)
    aout.enableChannel(0, True)
    aout.enableChannel(1, True)
    
    rnd_ricker = random_ricker()
    w1_data = rnd_ricker + vcm
    w2_data = vcm - rnd_ricker

    buffer = [w1_data, w2_data]
    aout.setCyclic(True)
    aout.push(buffer)
    print("Noiseless wavelet generated!")

    return w1_data, w2_data

def plotter(w1_data, w2_data):
    plt.plot(w1_data)
    plt.plot(w2_data)
    plt.plot(w1_data-w2_data)
    plt.show()

def noise_add(w1, w2):
    s1 = np.random.uniform(low = l, high = h, size = 375000)
    s2 = np.random.uniform(low = l, high = h, size = 375000)
    w1 += s1
    w2 += s2
    print("Noisy wavelet generated!")

    return w1, w2
    
def wav_gen_main():
    ctx = wav_init()
    w1, w2 = wavdiff_out(ctx)
    plotter(w1, w2)
    w3, w4 = noise_add(w1, w2)
    plotter(w3, w4)
    wav_close(ctx)

if __name__ == '__main__':
   wav_gen_main()
    
