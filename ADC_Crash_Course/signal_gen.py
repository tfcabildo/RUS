"""Add phase noise and distortion to the signal generation class. """

import numpy as np # Import NumPy library

class sine_sig_gen():
    """
    Attributes:
        N - Number of samples
        freq - signal frequency in Hertz
        phase - phase to be added directly to the fundamental (radians)
        fs - sample rate in samples per second
        signal_ampl - sinewave signal amplitude (Textbook definition - peak value away from zero)
        vref - ADC voltage reference, representing the peak-to-peak range of inputs
        t_noise - thermal noise in RMS volts.
        bits - ADC output will be quantized to 2**bits discrete values
        jitter - Sampling jitter in seconds RMS (integrated phase noise)
        harmonics - list of harmonic components. Each element is [amplitude, phase],
            where amplitude is fractional with respect to the fundamental and phase is in radians.
            First element represents the second harmonic
        quantize - whether or not to quantize values.
    
    Methods:
        generate - returns quantized ADC values as floating point array of length N,
        or unquantized floating point values if quantize attribute is set to False.
    """
    def __init__(self):
        self.N = 4096
        self.phase = 0.0
        self.fs = 100000
        bin_number = 5 # Start out with five cycles over the time record
        self.freq = self.fs * bin_number / self.N
        self.signal_ampl = 1.0
        self.vref = 5.0
        self.t_noise = 0.0 # 7.6e-6 # 1/10 lsb, @ 5V, 16 bits
        self.jitter = 0.0
        self.p_noise = 0.0
        self.harmonics = [[0.0, 1.0], [0.0, 2.0]] # Harmonic, each element is [fractional amplitude, phase]
        self.bits = 16
        self.quantize = True

    def generate(self):
    
        smp_times = np.arange(0, self.N/self.fs, 1.0/self.fs)
        """Sampling instants. We want N samples, taken at some sample rate fs in Hertz, which implies 1/fs
        seconds between samples. The NumPy arange function returns evenly spaced values within a given
        interval, which is exactly what we want."""

        smp_jitter = np.random.normal(loc=0, scale=self.jitter, size=self.N)
        """Jitter values. These are added to the sample times, with the effect that the sample times are
        "wiggled" around a bit. If the signal is slewing, the digitized amplitude will be affected. """
        
        smp_times += smp_jitter
        
        signal = self.signal_ampl * np.sin(2.0*np.pi*self.freq*smp_times+self.phase)
        """Okay, generate the signal. We are using the strict mathematical definition of amplitude, which
        is half of the peak-to-peak excursion of the signal. The sine function swings from -1.0 to +1.0,
        so no scaling factor is necessary.
        At this point, the signal is discrete in the time domain, because we've got a finite number of samples
        taken over the measurement interval. In the voltage domain, the precision is 64-bit floating
        point, MUCH finer than any real world ADC."""

        hindex = 0 
        for harmonic in self.harmonics:
            """Generate harmonics. Cycle through list of harmonic amplitudes and phases, and add
            them to the main signal."""

            hamp = self.signal_ampl * harmonic[0]

            hph = harmonic[1]

            hval = hamp * np.sin(2.0*np.pi*self.freq*(hindex + 2.0)*smp_times+self.phase+hph)
            #print("ampl, ph, a few values: ", hamp, hph, hval[:8])
            signal += hval # Add harmonic to signal
            hindex += 1
        
        noise = np.random.normal(loc=0, scale=self.t_noise, size=self.N)
        """ Random thermal noise. Set to zero if only modeling quantization noise. """
        signal += noise

        adc_inf_bits = ((signal / self.vref) * 2**self.bits)
        """THIS could be considered the "Fundamental ADC equation". An ADC performs the mathematical operation of
        division - the output code is proportional to the input voltage divided by the reference. Maybe with some
        offset, maybe with some scaling factor, but fundamentally, it's plain old division. The signal is mapped
        to digital values, in this case from -2**(bits-1) to 2**(bits-1). The bits-1 factor is because we've got
        a bipolar signal that swings from negative vref/2 to positive vref/2.
        Note the name of this variable, which implies an "infinity bit ADC". It's not really infinity bits, but
        in this case, a 64-bit float is close enough to infinity that we can assume it's infinity. """        

        adc_output = np.around(adc_inf_bits, decimals=0)

        if self.quantize:
            return adc_output
        else:
            return adc_inf_bits