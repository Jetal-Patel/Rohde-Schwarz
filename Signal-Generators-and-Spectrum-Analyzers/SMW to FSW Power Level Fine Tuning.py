"""This is an example to start at a certain CW output power on the SMW
and increment upwards until the desired power is achieved on the FSW.
"""

from RsInstrument import *
import time

from fontTools.misc.cython import returns

# Initialize the session
smw = RsInstrument('TCPIP::192.168.8.66::hislip0', reset=False)

smw.write('*RST')
idn = smw.query('*IDN?')
print(f"\nHello, I am: '{idn}'")

fsw = RsInstrument('TCPIP::192.168.8.108::hislip0', reset=False)

fsw.write('*RST')
idn = fsw.query('*IDN?')
print(f"\nHello, I am: '{idn}'")


TARGET_FSW_POWER = -1 # Set the desired power at the FSW
SMW_STARTING_POWER = -5 # Set the starting output power of the SMW
MAX_SMW_POWER = 0 # Set the max power the SMW will put out
CW_FREQUENCY = 1000000000 # Set the frequency of the CW signal
REF_LEVEL = TARGET_FSW_POWER + 10

smw.write_with_opc(f'SOUR1:POW:LEV:IMM:AMPL {SMW_STARTING_POWER}')
smw.write_with_opc('OUTP1:STAT 1')
fsw.write_with_opc('*CLS')
fsw.write_with_opc(':SYST:DISP:UPD ON')
fsw.write_with_opc(':INIT:CONT OFF')
fsw.write_with_opc(f':SENS:FREQ:CENT {CW_FREQUENCY}')
fsw.write_with_opc(':SENS:FREQ:SPAN 200000000')
fsw.write_with_opc('SENS:BAND:RES 1000000')
fsw.write_with_opc(f':DISP:WIND:TRAC:Y:SCAL:RLEV {REF_LEVEL}')
fsw.write_with_opc(':CALC1:MARK1:STAT ON')
fsw.write_with_opc(':CALC1:MARK1:MAX:PEAK')
fsw.write_with_opc(':INIT:IMM')
fsw.write_with_opc(':CALC1:MARK1:MAX:PEAK')
FSW_POWER = float (fsw.query(':CALC1:MARK1:Y?'))
SMW_OUT_PWR = SMW_STARTING_POWER

while abs(FSW_POWER - TARGET_FSW_POWER) >= 0.50:
    fsw.write_with_opc(':INIT:IMM')
    fsw.write_with_opc(':CALC1:MARK1:MAX:PEAK')
    FSW_POWER = float(fsw.query(':CALC1:MARK1:Y?'))
    if SMW_OUT_PWR < MAX_SMW_POWER:
        SMW_OUT_PWR += 0.25
        smw.write(f'SOUR1:POW:LEV:IMM:AMPL {SMW_OUT_PWR}')
        time.sleep(0.5)
    else:
        print("SMW Power has reached user defined limit")
        break

else: print("FSW Power is now at the desired level!")

smw.close()
fsw.close()
