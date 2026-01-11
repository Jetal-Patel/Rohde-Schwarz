"""This is an example script to connect to the NRPxxS sensor and take continuous average measurements in intervals.
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
from tkinter import *
import time

# Initialize the session
NRP40S = RsInstrument('USB::0x0AAD::0x015F::101469::INSTR', reset=False)

NRP40S.write_with_opc('*RST')
idn = NRP40S.query_with_opc('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(NRP40S.instrument_options)}')

NRP40S.write_with_opc('*RST')
NRP40S.write_with_opc('UNIT:POW DBM') # Sets the units to dBm

# Zero the Sensor
root = Tk()
myLabel = Label(root, text="Please turn the source off so the sensor can be Zeroed")
myLabel.pack()

myButton = Button(root, text = "Okay!", command = root.destroy)
myButton.pack()
root.mainloop()

NRP40S.write_with_opc('CAL1:ZERO:AUTO ONCE')

#Turn on RF Source and take measurements
root = Tk()
myLabel2 = Label(root, text= "Please turn on the RF Source")
myLabel2.pack()

myButton2 = Button(root, text = "Okay!", command = root.destroy)
myButton2.pack()
root.mainloop()

# Take Measurements in intervals and then output the result
for i in range(10):
    time.sleep(1)
    NRP40S.write_with_opc('INIT:IMM')
    print(NRP40S.query_with_opc('FETCH?'))



# Close the session
NRP40S.close()
