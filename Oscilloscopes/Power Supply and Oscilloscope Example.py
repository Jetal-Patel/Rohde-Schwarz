''' This is an example script to generate with the HMP Power Supply
and analyze on the MXO5 Oscilloscope'''

from RsInstrument import *
import time
# Set up communication with the instruments
resource = 'TCPIP::10.10.10.5::5025::SOCKET'  # Assign Instrument VISA resource string
hmp = RsInstrument(resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")

def comprep():
    """Preparation of the communication (termination, etc...)"""
    hmp.visa_timeout = 3000  # Timeout for VISA Read Operations
    hmp.opc_timeout = 3000  # Timeout for opc-synchronised operations
    hmp.clear_status()  # Clear status register

mxo5 = RsInstrument('TCPIP::10.10.10.7::hislip0', reset=False)

hmp.write_str('*RST') # Preset the HMP

mxo5.write_with_opc('*RST') # Preset the Oscilloscope
mxo5.write_with_opc('SYST:DISP:UPD ON') # Turn on the display
mxo5.write_with_opc('TRIGger:MODE NORMal') # Avoid triggering in Auto mode
mxo5.write_with_opc('TIM:SCAL 1') # 1 second per division
mxo5.write_with_opc('CHAN1:BAND 20 MHz') # 20MHz measurement bandwidth
mxo5.write_with_opc('HDEF:BWID 10000') # 10kHz HD mode filter bandwidth
mxo5.write_with_opc('HDEF:STAT ON') # Turn on HD mode
current = 0.005 # Current is set to 5mA
voltage = 0.050 # Set voltage to 10mV
hmp.write_str(f'SOUR:VOLT:LEV:IMM:AMPL {voltage}') # Set Voltage to 12 Volts
hmp.write_str(f':SOUR:CURR:LEV:IMM:AMPL {current}') # Set Current to 75mA


mxo5.write_with_opc('RUN') # Start the sweep
hmp.write_str('OUTP 1') # Turn Channel 1 Output On
hmp.write_str('SOUR:VOLT:LEV:IMM:AMPL 0.075') # Increase voltage to 75mV
time.sleep(2)
hmp.write_str('SOUR:VOLT:LEV:IMM:AMPL 0.1') # Increase voltage to 100mV
time.sleep(2)
hmp.write_str('SOUR:VOLT:LEV:IMM:AMPL 0.125') # Increase voltage to 125mV
time.sleep(2)
hmp.write_str('SOUR:VOLT:LEV:IMM:AMPL 0.150') # Increase voltage to 150mV
time.sleep(4)
mxo5.write_with_opc('STOP') # Stop the sweep