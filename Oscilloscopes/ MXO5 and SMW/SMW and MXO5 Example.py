''' This is an example script to generate a CW on the SMW200A
and analyze on the MXO5 Oscilloscope
'''

from RsInstrument import *
import matplotlib.pyplot as plt
import time

mxo5 = RsInstrument('TCPIP::10.10.10.7::hislip0', reset=False)
smw = RsInstrument('TCPIP::10.10.10.6::hislip0', reset=False)

# SMW and MXO Initialization
smw.write_with_opc('*RST') # Preset
mxo5.write_with_opc('*RST') # Preset the Oscilloscope

# SMW Configuration
smw.write_with_opc('SOUR1:FREQ:CW 100000000') # Set SMW to 500MHz
smw.write_with_opc('SOUR1:POW:LEV:IMM:AMPL -10') # Set Amplitude to -10dBm
smw.write_with_opc('OUTP:STAT 1') # Turn on RF Output

# MXO Configuration and Capture
mxo5.write_with_opc('SYST:DISP:UPD ON') # Turn on the display
mxo5.write_with_opc('TIM:SCAL 100E-9')
mxo5.write_with_opc('TRIGger:MODE NORMal') # Avoid triggering in Auto mode
mxo5.write_with_opc("RUNsingle") # Single Sweep
mxo5.write_str("FORMat:DATA REAL,32;:FORMat:BORDer LSBFirst")
mxo5.bin_float_numbers_format = BinFloatFormat.Single_4bytes
mxo5.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
print('Now start to transfer binary waveform data. Please wait for about 20 seconds...')
data_bin = mxo5.query_bin_or_ascii_float_list("CHAN:DATA?")


# Plot The Results
plt.figure(1)
plt.plot(data_bin)
plt.title('Binary waveform')
plt.ylabel("Amplitude (Volts)")
plt.xlabel("Sample #")
plt.show()

mxo.close()
smw.close()
