"""This is an example for testing P1dB of your amplifier with a
SMB100B Signal Generator, FSW Spectrum Analyzer, and HMP Power Supply.

"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
import time
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

# Initialize the session and set up instrument connections
fsw = RsInstrument('TCPIP::10.10.10.3::hislip0', reset=False)
idn = fsw.query_with_opc('*IDN?')
smb = RsInstrument('TCPIP::10.10.10.2::hislip0', reset=False)

resource = 'TCPIP::10.10.10.4::5025::SOCKET'  # Assign Instrument VISA resource string
hmp = RsInstrument(resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")

def comprep():
    """Preparation of the communication (termination, etc...)"""
    hmp.visa_timeout = 3000  # Timeout for VISA Read Operations
    hmp.opc_timeout = 3000  # Timeout for opc-synchronised operations
    hmp.clear_status()  # Clear status register


# Initialize the instruments
smb.write_with_opc('*RST')
fsw.write_with_opc('*RST')
hmp.write_str('*RST') # Preset the HMP

frequency = 1500000000 # Frequency is 1.5GHz
start_power_1 = -25 # Start Input Power of -25dBm for the 1dB steps
stop_power_1 = -5 # Stop Input Power of -5dBm for the 1dB steps
start_power_point1 = -4.9 # Start Input Power of -4.9dBm for the 0.1dB steps
stop_power_point1 = 2 # Stop Input Power of 2dBm for the 0.1dB steps
bias_voltage = 12 # Bias voltage of 12V
bias_current = 0.075 # Bias current of 75mA

# Set up the measurement

# Make connections
root = Tk()
myLabel = Label(root, text="Please Connect the SMB100B RF Output to the Amplifier RF Input. Then connect the Amplifier RF Output to the FSW RF Input. Then connect the DC Power Supply Channel 1 Output to the Amplifier DC Input)")
myLabel.pack()



myButton = Button(root, text = "Okay!", command = root.destroy)
myButton.pack()
root.mainloop()

# Turn on Power Supply
hmp.write_str(f'SOUR:VOLT:LEV:IMM:AMPL {bias_voltage}') # Set Voltage to 12 Volts
hmp.write_str(f':SOUR:CURR:LEV:IMM:AMPL {bias_current}') # Set Current to 75mA
hmp.write_str('OUTP 1') # Turn Channel 1 Output On


# Set up fsw
fsw.write_with_opc('*CLS') # Clear status registers
fsw.write_with_opc(':SYST:DISP:UPD ON') # Turn on the display
fsw.write_with_opc(':INIT:CONT OFF')
fsw.write_with_opc(f'SENS:FREQ:CENT {frequency}') # Set center frequency on FSW
fsw.write_with_opc('SENS:FREQ:SPAN 100000000') # Set span to 100MHz
fsw.write_with_opc('INP:ATT:AUTO OFF') # Set Attenuation to Manual
fsw.write_with_opc('INP:ATT 30') # Set Attenuation to 30dB
fsw.write_with_opc('DISP:WIND:TRAC:Y:SCAL:RLEV 30') # Set Reference Level to 30dBm
fsw.write_with_opc('SENS:BAND:RES 100000') # Set RBW to 100kHz
fsw.write_with_opc('INIT:IMM') # Take single sweep
fsw.write_with_opc(':CALC1:MARK1:STAT ON') # Turn Marker 1 On

# Set up SMB100B
smb.write_with_opc(f'SOUR1:FREQ:CW {frequency}') # Set SMB100B to 1.5GHz
smb.write_with_opc(f'SOUR1:POW:LEV:IMM:AMPL {start_power_1}') # Set SMB100B initial power to -25dBm
smb.write_with_opc('OUTP1:STAT 1') # Turn SMB RF On

# Set up float range for the 0.1dB steps
def float_range(start,stop,step):
    while start <= stop:
        yield start
        start += step


# Create arrays for Input Powers, Output Powers, and Gain
Output_Powers1 =np.array([], dtype = float) # Create an empty list for output powers
Gain1 = np.array([], dtype = float) # Create an empty list for the Gain
Input_Powers1 =np.array([], dtype = float) # Create an empty list for input powers


# Step through the power levels in 1dB steps and record the output power on the fsw
for i in range (start_power_1, stop_power_1 + 1, 1):
    smb.write_with_opc(f':SOUR1:POW:LEV:IMM:AMPL {i}') # Set SMB100B power
    time.sleep(1)
    print (i)
    fsw.write_with_opc('INIT:IMM') # Take single sweep
    fsw.write_with_opc('CALC1:MARK1:MAX:PEAK') # Set Marker to Peak
    Output_Power = float(fsw.query_with_opc('CALC1:MARK1:Y?')) # Append the list with the queried power level
    Output_Powers1 = np.append(Output_Powers1, [Output_Power])
    Gain1 = np.append(Gain1, [Output_Power - i])
    Input_Powers1 = np.append(Input_Powers1, [i])

for i in float_range (start_power_point1, stop_power_point1, 0.1):
    smb.write_with_opc(f':SOUR1:POW:LEV:IMM:AMPL {i}') # Set SMB100B power
    time.sleep(1)
    print (i)
    fsw.write_with_opc('INIT:IMM') # Take single sweep
    fsw.write_with_opc('CALC1:MARK1:MAX:PEAK') # Set Marker to Peak
    Output_Power = float(fsw.query_with_opc('CALC1:MARK1:Y?'))  # Append the list with the queried power level
    Output_Powers1 = np.append(Output_Powers1, [Output_Power]) # Append the list with the queried power level
    Gain1 = np.append(Gain1, [Output_Power - i])
    Input_Powers1 = np.append(Input_Powers1, [i])

hmp.write_str('OUTP GEN OFF') # Turn off HMP Outputs
smb.write_with_opc('OUTP1:STAT 0') # Turn off SMB100B RF Output



Linear_Gain = Gain1[0]
target_gain = Gain1[0] - 1
num_points = abs(start_power_1 - stop_power_1) + (abs(start_power_point1 - stop_power_point1) * 10)

for i in range (0,int(num_points)):
    if (Gain1[i] < target_gain):
        print (f"Linear Gain is: {Linear_Gain} dB")
        print (f"P1dB occurs where Gain is: {Gain1[i]} dB")
        print (f"The IP1dB is: {Input_Powers1[i]} dBm.")
        print (f"The OP1dB is: {Output_Powers1[i]} dBm")
        input_marker = Input_Powers1[i]
        output_marker = Output_Powers1[i]
        gain_marker = Gain1[i]
        break


# Plot the traces
plt.figure()
plt.plot(Input_Powers1, Output_Powers1)
plt.xlabel("Input Power (dBm)")
plt.ylabel("Output Power (dBm)")
plt.title("Input Power vs Output Power (Range1)")
plt.plot([input_marker], [output_marker], marker='o', markersize=10, color='red', label='P1dB')

plt.figure()
plt.plot(Input_Powers1, Gain1)
plt.xlabel("Input Power (dBm)")
plt.ylabel("Output Power (dBm)")
plt.title("Input Power vs Gain (Range1)")
plt.plot([input_marker], [gain_marker], marker='o', markersize=10, color='red', label='P1dB')


plt.show()


smb.close()
fsw.close()
