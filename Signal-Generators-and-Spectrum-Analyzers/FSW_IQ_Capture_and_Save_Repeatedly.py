"""This example takes IQ Captures based on when
the spectrum reaches a minimum power level in the measured span
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *
stringA = "keep running"
min = -50 # defines the minimum value to "trigger on"
count = 1
# Initialize the session
fsw = RsInstrument('TCPIP::192.168.1.71::hislip0', reset=False)

fsw.write_with_opc('*RST') # Preset the FSW
fsw.write_with_opc('SYST:DISP:UPD ON') # Turn on the display

# Set up the Spectrum Mode
fsw.write_with_opc(':SENS:FREQ:CENT 1000000000') # Set Center Freq to 1GHz
fsw.write_with_opc(':SENS:FREQ:SPAN 800000000') # Set Span to 800MHz
fsw.write_with_opc('INP:ATT 15') # Set Input Attenuation to 15dB
fsw.write_with_opc('INP:GAIN:STAT ON') # Set Preamp On
fsw.write_with_opc(':SENS:WIND1:DET1:FUNC POS') # Set Trace Detector to Positive Peak
fsw.write_with_opc(':INIT:CONT OFF') # Single sweep mode
fsw.write_with_opc(':INIT:IMM') # Initiate a single sweep
fsw.write_with_opc(':CALC1:MARK1:STAT ON') # Turn on Marker 1
fsw.write_with_opc(':CALC1:MARK1:MAX:PEAK') # Set Marker to Peak

# Create new IQ ANALYZER Window
fsw.write_with_opc(f"INST:CRE:NEW IQ,'IQ Analyzer'") # Open I/Q Analyzer mode
fsw.write_with_opc('INIT:CONT OFF') # Single sweep mode
fsw.write_with_opc('DISP:WIND:TRAC:Y:SCAL:RLEV -15') # Reference Level is -10dBm
fsw.write_with_opc('INP:ATT:AUTO OFF') # Auto Attenuation OFF
fsw.write_with_opc(':INP:ATT 15') # Input Attenuation to 15dB
fsw.write_with_opc('INP:GAIN:STAT ON') # Turn on the preamp

fsw.write_with_opc('SENS:FREQ:CENT 1000000000') # Set Center Frequency to 1GHz
fsw.write_with_opc('TRAC:IQ:SRAT 800000000') # Set SRate to 800MHz
fsw.write_with_opc('SENS:SWE:TIME 0.8') # Set meas time to 0.8 seconds
fsw.write_with_opc(':SENS:WIND1:DET1:FUNC POS') # Positive Peak Detector




def IQ_Capture(N):
    fsw.write_with_opc("INST:SEL 'IQ Analyzer'")
    directory = "C:\\R_S\\instr\\user\\"
    filename = f"Capture_{N}"
    try:
        fsw.write_with_opc('INIT:IMM', timeout=1500000000) # Take a single sweep
        print("Took IQ Capture")
        fsw.write_with_opc(f"MMEM:STOR:IQ:STAT 1,'{directory}''{filename}'", timeout=1500000000)# Needs to be a different filename each time
        print("IQ Capture Save Successful")
    except:
        print("Could not take IQ Capture in Time")
def Sweep_Spectrum(x):
    fsw.write_with_opc('INIT:IMM')  # Run single sweep
    fsw.write_with_opc('CALC1:MARK1:MAX:PEAK')  # Set marker to peak
    current_peak = float(fsw.query_with_opc('CALC1:MARK1:Y?'))  # Query the Peak
    if current_peak > x:
        return 1
    else:
        return 0

while stringA != "stop":

    fsw.write_with_opc("INST:SEL 'Spectrum'") # Select Spectrum Mode
    if Sweep_Spectrum(min) == 1:
        IQ_Capture(count)
        count+=1
    else:
        Sweep_Spectrum(min)



# Close the session
fsw.close()
