"""This is an example script to measure multiple channels at different frequencies and bands
on the FPH Spectrum Rider
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
import time
# Initialize the session
fph = RsInstrument('TCPIP::192.168.58.70::hislip0', reset=False)

fph.write_with_opc('*RST') # Reset the FPH
idn = fph.query('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(fph.instrument_options)}')


# SET UP THE MULTICHANNEL MEASUREMENTS AT 20GHZ CF
fph.write_with_opc('CALC:MARK:FUNC:POW:SEL ACP') # Set measurement mode to ACLR
fph.write_with_opc('SENS:FREQ:CENT 20000000000') # Set center frequency to 20 GHz
fph.write_with_opc(':SENS:FREQ:SPAN 401000000') # Set span to 401 MHz
# fph.write_with_opc('DISP:TRAC:MODE WRIT') # Sets the trace mode to clear/write
fph.write_with_opc('DISP:TRAC:Y:SCAL:RLEV -10') # Sets the reference level to -10dBm
fph.write_with_opc('INP:ATT 0') # Sets the input attenuation
fph.write_with_opc('INP:GAIN:STAT OFF') # Sets the preamplifier to OFF
fph.write_with_opc('BAND 300 kHz') # Sets the RBW to 300 kHz
fph.write_with_opc('BAND:VID 1 MHz') # Sets the VBW to 1 MHz
fph.write_with_opc('SWE:TIME:AUTO ON') # Sets sweep time to auto
fph.write_with_opc(':SENS:FREQ:MODE SWE') # Sets mode to sweep
fph.write_with_opc('POW:ACH:TXCH:COUN 12') # Sets 12 TX channels
fph.write_with_opc('POW:ACH:ACP 4') # Sets 8 adjacent channels. 4 upper and 4 lower
fph.write_with_opc('POW:ACH:SPAC:CHAN 20000000') # Sets the channel spacings to 20 MHz
fph.write_with_opc('POW:ACH:SPAC 20000000') # Sets the spacing to 20 MHz between Tx and Adj
fph.write_with_opc('POW:ACH:BAND:CHAN 20000000') # Sets the channel bandwidths to 20 MHz
fph.write_with_opc('POW:ACH:BAND:ACH 20000000') # Sets the adjacent channel bandwidths to 20MHz.
fph.write_with_opc('POW:ACH:MODE ABS') # Shows absolute power of all channels

# Initiate SINGLE SWEEP
fph.write_with_opc('INIT:CONT OFF') # Set to single sweep mode
fph.write_with_opc('INIT:IMM') # Initiate a single sweep

# RESULTS QUERY, SORT, AND PRINT
results = fph.query('CALC:MARK:FUNC:POW:RES? ACP') # Query the channel powers
ChannelPowers = results.split(",")
print("ChannelPowers = " + results)
ChannelNames = ["Tx1" , "Tx2" , "Tx3" , "Tx4" , "Tx5" , "Tx6" , "Tx7" , "Tx8" , "Tx9" , "Tx10" , "Tx11" , "Tx12" ,
"Total" , "AdjLower" , "AdjUpper" , "Alt1Lower" , "Alt1Upper" , "Alt2Lower" , "Alt2Upper" , "Alt3Lower" , "Alt3Upper"]

ChannelResults = []
Channel1 = ChannelPowers[19]
ChannelResults.append(Channel1)
Channel2 = ChannelPowers[17]
ChannelResults.append(Channel2)
Channel3 = ChannelPowers[15]
ChannelResults.append(Channel3)
Channel4 = ChannelPowers[13]
ChannelResults.append(Channel4)
Channel5 = ChannelPowers[0]
ChannelResults.append(Channel5)
Channel6 = ChannelPowers[1]
ChannelResults.append(Channel6)
Channel7 = ChannelPowers[2]
ChannelResults.append(Channel7)
Channel8 = ChannelPowers[3]
ChannelResults.append(Channel8)
Channel9 = ChannelPowers[4]
ChannelResults.append(Channel9)
Channel10 = ChannelPowers[5]
ChannelResults.append(Channel10)
Channel11 = ChannelPowers[6]
ChannelResults.append(Channel11)
Channel12 = ChannelPowers[7]
ChannelResults.append(Channel12)
Channel13 = ChannelPowers[8]
ChannelResults.append(Channel13)
Channel14 = ChannelPowers[9]
ChannelResults.append(Channel14)
Channel15 = ChannelPowers[10]
ChannelResults.append(Channel15)
Channel16 = ChannelPowers[11]
ChannelResults.append(Channel16)
Channel17 = ChannelPowers[14]
ChannelResults.append(Channel17)
Channel18 = ChannelPowers[16]
ChannelResults.append(Channel18)
Channel19 = ChannelPowers[18]
ChannelResults.append(Channel19)
Channel20 = ChannelPowers[20]
ChannelResults.append(Channel20)

for i in range (len(ChannelResults)):
    print (f"Channel {i+1}  =  {ChannelResults[i]} dBm \n")


# Close the session
fph.close()
