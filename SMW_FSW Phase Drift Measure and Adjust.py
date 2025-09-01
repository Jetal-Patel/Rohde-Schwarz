"""This is a Hello-World example for communicating with your FSW-85 instrument.
The field 'Alias' defines the variable name with which 
you are going to address the instrument in your python scripts.
For the FSW-85, the alias is 'fsv'
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
import matplotlib.pyplot as plt
import time


# Initialize the session
fsv = RsInstrument('TCPIP::fsv-101787.local::hislip0', reset=False)

fsv.write('*RST')
idn = fsv.query('*IDN?')
print(f"\nHello, I am: '{idn}'")

smbv = RsInstrument('TCPIP::100.100.100.9::5025::SOCKET', reset=False)

smbv.write('*RST')
idn = smbv.query('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(smbv.instrument_options)}')



# Enter your code here...
fsv.write(':SYST:DISP:UPD ON')
fsv.write(':INIT:CONT OFF')
fsv.write(':INP:TYPE INPUT2')
fsv.write(':SENS:FREQ:CENT 1000000000')
fsv.write(':INST:CRE:NEW IQ, "IQ Analyzer"')
fsv.write(":LAY:REPL:WIND '1',PHASE")
fsv.write(':DISP:WIND1:SUBW:TRAC1:Y:SPAC LDB')
fsv.write(':SENS:ROSC:SOUR E10')
fsv.write(':SENS:ROSC:LBW 100')
fsv.write(':TRAC:IQ:SRAT 1000000')
fsv.write(':CALC:MARK:STAT 1')
fsv.write(':CALC:MARK:MAX:PEAK')

#Fetch Phase data from FSW and write to array.
data = []
x = []
z = fsv.query(':CALC1:MARK1:Y?') # Find the initial phase
for i in range(3600): # Number of seconds to run test for
    time.sleep(1) # Interval in seconds between each fetch of phase data
    x.append(i)
    current = fsv.query(':CALC1:MARK1:Y?')
    data.append(current)
    inv = (current * -1)
    smbv.write(f"SOUR1:PHAS {inv}")

#Convert radians to degrees
m = float(57.2957795)
datas = [float(s) for s in data]
result = []
for element in datas:
    result.append(element * m)


#Print Results

plt.plot(x,result)
plt.title("Phase Plot")
plt.xlabel('Time(s)')
plt.ylabel('Phase(degrees)')
plt.show()
#print (result)
# Close the session
fsv.close()
