"""This is an example script to step frequency in the SMW200A and do a max hold on the FSW
which sweeps every time a step occurs.
This is for troubleshooting purposes
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
import time
# Initialize the session
smw = RsInstrument('TCPIP::10.10.10.6::hislip0', reset=False)

smw.write('*RST')
idn = smw.query('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(smw.instrument_options)}')

fsw = RsInstrument('TCPIP::10.10.10.7::hislip0', reset=False)
fsw.write_with_opc('SYST:DISP:UPD ON') # Turn on the display
fsw.write_with_opc('SENS:FREQ:STAR 325000000') # Start Frequency of 325MHz
fsw.write_with_opc('SENS:FREQ:STOP 10175000000') # Stop Frequency of 10.175GHz
fsw.write_with_opc('DISP:WIND1:SUBW:TRAC1:MODE MAXH') # Max Hold Trace 1
fsw.write_with_opc('DISP:WIND1:TRAC1:MODE:HCON ON') # Turn Hold to ON

smw.write_with_opc('SOUR1:POW:LEV:IMM:AMPL -10') # Set SMW200A Power Level to -10dBm
smw.write_with_opc('SOUR1:FREQ:CW 325000000') # Set starting freq of the SMW200A
smw.write_with_opc('OUTP:STAT 1') # Turn RF ON
for i in range (325000000,10175000000, 1000000,):
    smw.write_with_opc(f'SOUR1:FREQ:CW {i}') # Write i as the SMW frequency
    time.sleep(0.2)

# Enter your code here...


# Close the session
smw.close()
