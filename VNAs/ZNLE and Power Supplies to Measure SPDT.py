"""This is an example script to calibrate the ZNLE with the ZN-ZExxx
and then measure a SPDT using two power supplies and the ZNLE.
For the ZNLE6-2Port, the alias is 'znle'
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
import time
from tkinter import *
# Initialize the session

znle = RsInstrument('TCPIP::10.10.10.6::hislip0', reset=False)

znle.write('*RST')
znle.write('SYST:DISP:UPD ON')
idn = znle.query('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(znle.instrument_options)}')

resource = 'TCPIP::10.10.10.5::5025::SOCKET'  # Assign Instrument VISA resource string
hmp = RsInstrument(resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")

def comprep():
    """Preparation of the communication (termination, etc...)"""
    hmp.visa_timeout = 3000  # Timeout for VISA Read Operations
    hmp.opc_timeout = 3000  # Timeout for opc-synchronised operations
    hmp.clear_status()  # Clear status register

ngl = RsInstrument('TCPIP::10.10.10.4::hislip0', reset=True)


# Set up the channel on the VNA
znle.write('*RST')
znle.write('SENS:FREQ:STAR 750000') # Start Frequency of 7500kHz
znle.write('DISPLAY:WINDOW2:STATE ON') # Add a second window
znle.write('CALCULATE1:PARAMETER:SDEFINE "Trc2","S11"') # Add trace for S11
znle.write('DISPLAY:WINDOW2:TRACE2:FEED "Trc2"') # Feed Trace 2 to Window 2

znle.write('INIT:CONT:ALL OFF')
znle.write_with_opc(':INIT')

root = Tk()
myLabel = Label(root, text="Please connect Port 1 of the VNA to Port 1 of the Autocal and Port 2 of the VNA to Port 2 of the Autocal.")
myLabel.pack()

myButton = Button(root, text = "Okay!", command = root.destroy)
myButton.pack()
root.mainloop()


string1 = znle.query('SENS:CORR:COLL:AUTO:PORT:CONN?')
root = Tk()
myLabel2 = Label(root, text= f"You have the ports connected in the following configuration: {string1} . If it's not (1,1,2,2), please change your configuration")
myLabel2.pack()

myButton2 = Button(root, text = "Okay!", command = root.destroy)
myButton2.pack()
root.mainloop()


znle.write_with_opc("SENS:CORR:COLL:AUTO:CONF FNP,'Factory'")
znle.write_with_opc("SYST:COMM:RDEV:AKAL:ADDR 'ZN-ZE126::100132'")
znle.write_with_opc("SENS:CORR:COLL:AUTO:PORTS:TYPE FNP,'',1,1,2,2")

znle.write('INIT:CONT:ALL OFF')
znle.write_with_opc(':INIT')

root = Tk()
myLabel3 = Label(root, text= f"Disconnect the calibration kit and connect the switch and power supplies." ) # Connect the switch
myLabel3.pack()

myButton3 = Button(root, text = "Okay!", command = root.destroy)
myButton3.pack()
root.mainloop()


# Turn on Power Supplies
hmp.write_str('*RST') # Reset the Power Supply
hmp.write_str('INST:NSEL 2') # Select Channel 2
hmp.write_str('SOUR:VOLT:LEV:IMM:AMPL 5') # Set Voltage to 5V
hmp.write_str(':SOUR:CURR:LEV:IMM:AMPL 0.05') # Set Current to 50mA
hmp.write_str('OUTP:SEL 1') # Turn on selected channel
hmp.write_str('OUTP:GEN 1') # Turn Output On

ngl.write_str('*RST') # Reset the NGL
ngl.write_str('SOUR:VOLT:LEV:IMM:AMPL 3') # Set the voltage to 3 volts
ngl.write_str(':SOUR:CURR:LEV:IMM:AMPL 0.001') # Set the current to 1mA
ngl.write_str('OUTP:STAT ON') # Turn on Output



root = Tk()
myLabel4 = Label(root, text= f"The ZNLE will now measure the switch in the RF2 Position." ) # Connect the switch
myLabel4.pack()

myButton4 = Button(root, text = "Okay!", command = root.destroy)
myButton4.pack()
root.mainloop()

znle.write_with_opc('INIT:IMM') # Take Single Sweep



hmp.close()
# Close the session
znle.close()
