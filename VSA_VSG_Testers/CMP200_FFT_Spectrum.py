"""This is an example script to Generate an ARB waveform on the CMP200, analyse the FFT Spectrum,
and then plot the data.
For the CMP200, the alias is 'cmp'
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
import matplotlib.pyplot as plt

# Initialize the session
cmp = RsInstrument('TCPIP::10.10.10.2::hislip0', reset=False)

cmp.write('*RST')
idn = cmp.query('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(cmp.instrument_options)}')

# Set up Generation
cmp.write_with_opc('SOUR:GPRF:GEN:BBM ARB') # Activate Arb Mode
cmp.write_with_opc('SOUR:GPRF:GEN:ARB:FILE "@WAVEFORM/NR_FR2_UL_QPSK_100MHz_SCS_120KHz.wv"') # Choose .wv file
cmp.write_with_opc('CONF:GPRF:GEN:SPAT:BCSW OFF') # Select a single output signal path
cmp.write_with_opc('ROUT:GPRF:GEN:SPAT "Port1.IFOut"') # Generate from IF OUT on Port 1
cmp.write_with_opc('SOUR:GPRF:GEN:RFS:FREQ 8.000000E+009') # Generator Frequency 8GHz
cmp.write_with_opc('SOUR:GPRF:GEN:RFS:LEV -30') # -30dBm Output Power


# Set up Measurement
cmp.write_with_opc('ROUT:GPRF:MEAS:SPAT "Port1.IFIn"') # Measure on Port 1 IF In
cmp.write_with_opc('CONF:GPRF:MEAS:RFS:FREQ 8E+9') # Measure at 8GHz Center Frequency
cmp.write_with_opc('CONF:GPRF:MEAS:FFTS:FSP 1E+9') # Measure with a span of 1GHz
cmp.write_with_opc('CONF:GPRF:MEAS:FFTS:FFTL MAX') # Max FFT length
cmp.write_with_opc('CONF:GPRF:MEAS:FFTS:DET RMS') # RMS Detector
cmp.write_with_opc('CONF:GPRF:MEAS:FFTS:AMOD LOG') # Log Averaging
cmp.write_with_opc('CONF:GPRF:MEAS:FFTS:MOEX ON') # Keep results even if faulty or inaccurate
cmp.write_with_opc('CONF:GPRF:MEAS:FFTS:REP SING') # Single Sweep


# Generate and then take single sweep
cmp.write_with_opc('SOUR:GPRF:GEN:STAT ON') # Switch on the Generator
cmp.write_with_opc('INIT:GPRF:MEAS:FFTS') # Start a measurement
long_string = cmp.query('READ:GPRF:MEAS1:FFTSanalyzer:POWer:AVERage?') # Read the measured FFT Spectrum Data
print ()
print (long_string)

float_array = [float(x) for x in long_string.split(',')]
print(float_array)
data_points = []
float_array.pop(0)

for i in range(0,len(float_array)):
    data_points.append(i)
    print(i)


plt.figure()
plt.plot(data_points, float_array)
plt.xlabel("Points")
plt.ylabel("Power(dBm)")
plt.title("FFT Spectrum on CMP200")

plt.show()
# Close the session
cmp.close()
