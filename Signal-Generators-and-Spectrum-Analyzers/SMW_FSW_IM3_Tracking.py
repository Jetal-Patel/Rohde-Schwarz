from RsInstrument import *
import time

# Set Instrument IP Addresses
smw_ip_address = r'172.21.147.198'
fsw_ip_address = r'172.21.147.197'

# Initialize Instruments
smw = RsInstrument(f"TCPIP::{smw_ip_address}::hislip0", reset=False)
fsw = RsInstrument(f"TCPIP::{fsw_ip_address}::hislip0", reset=False)

smw.write('*RST')
idn = smw.query('*IDN?')
print(f"\nHello, I am: '{idn}'")

fsw.write('*RST')
idn = fsw.query('*IDN?')
print(f"\nHello, I am: '{idn}'")

# Define tone spacings list
tonespacing = [10000000, 100000000, 200000000, 500000000]

# Set SMW 2-Tone Signal
smw.write('SOUR1:BB:MCCW:CARR:COUN 2') # 2 Tones in MCCW mode
smw.write('SOUR1:FREQ:CW 10000000000') # Center Frequency of 10GHz
smw.write('SOUR1:BB:MCCW:STAT 1') # Turn on MCCW
smw.write('SOUR1:POW:LEV:IMM:AMPL -10') # Set RMS RF Level to -10dBm
smw.write('OUTP:STAT 1') # Turn on RF Output

# Set FSW Measurement Parameters
fsw.write(':SENS:FREQ:CENT 10000000000') # Center Frequency of 10GHz
fsw.write(':SENS:FREQ:SPAN 2500000000') # Span of 2.5GHz
fsw.write(':SENS:BAND:RES 10000') # RBW of 10kHz
fsw.write(':INIT:CONT OFF') # Single Sweep Mode
fsw.write(':DISP:WIND1:SUBW:TRAC1:Y:SCAL 120')
# Iterate through the tone spacings and measure
for i in range(len(tonespacing)):
    smw.write_with_opc(f'SOUR1:BB:MCCW:CARR:SPAC {tonespacing[i]}  ')
    time.sleep(2)
    fsw.write_with_opc(':INIT:IMM; *WAI')
    fsw.write_with_opc(':CALC:MARK:FUNC:TOI:STAT ON')
    fsw.write_with_opc(':CALC1:MARK2:FUNC:TOI:SEAR ONCE')
    time.sleep(2)

smw.close()
fsw.close()