#This program is an example to measure the gain of an RF amplifier
# using the ZNB3000 Vector Network Analyzer and NGE100 Power Supply



from RsInstrument import *
import time
from tkinter import *

# Initialize the session
nge = RsInstrument('TCPIP::100.100.100.5::hislip0', reset=False)
znb = RsInstrument('TCPIP::100.100.100.7::hislip0', reset=False)




#Connect Calibration Kit
root = Tk()
myLabel = Label(root, text="Please Connect the Calibration Kit")
myLabel.pack()



myButton = Button(root, text = "Okay!", command = root.destroy)
myButton.pack()
root.mainloop()


#VNA Initial Setup
znb.write_with_opc('*RST')
znb.write_with_opc('SYST:DISP:UPD ON')
znb.write_with_opc(':INIT:CONT OFF')

#VNA Channel Setup
znb.write_with_opc('SENS1:FREQ:STAR 100000000')
znb.write_with_opc('SENS1:FREQ:STOP 26000000000')
znb.write_with_opc('SENS1:SWE:STEP 100000000')

#VNA Calibration
znb.write_with_opc("SENS1:CORR:COLL:AUTO:CONF FNP,'Factory'")
znb.write_with_opc("SYST:COMM:RDEV:AKAL:ADDR 'ZN-Z54-92::101005'")
znb.write_with_opc('CONF:CHAN1:STAT OFF')
znb.write_with_opc("DISPlay:LAYout:EXECute '(2,1,0,0,2(1,1,0,0,[]))'")
znb.write_with_opc("DISPlay:LAYout:EXECute '(1,2,0,0,2(1,1,0,0,[]))'")
znb.write_with_opc("SENSe1:CORRection:COLLect:AUTO:ASSignment1:DEFine 1, 1, 2, 2")
znb.write_with_opc("SENSe1:CORRection:COLLect:AUTO:ASSignment1:ACQuire")
time.sleep(3)
znb.write_with_opc("SENSe1:CORRection:COLLect:AUTO:SAVE")


znb.write_with_opc(':INIT:CONT ON')
znb.write_with_opc('SENS1:SWE:TYPE POW')
znb.write_with_opc('SOUR1:POW1:STOP -15.000000000000')
znb.write_with_opc('SENS1:FREQ:CW 1000000000')
znb.write_with_opc("CALC1:PAR:DEL 'Trc2'")


#Connect coax to the DUT
root = Tk()
myLabel2 = Label(root, text= "Please Connect the coax cables to the DUT")
myLabel2.pack()

myButton2 = Button(root, text = "Okay!", command = root.destroy)
myButton2.pack()
root.mainloop()

nge.write('*RST')
nge.write_with_opc('INST OUT1')
nge.write_with_opc('APPLY "12,0.077"')
nge.write_with_opc('OUTP:SEL 1')
nge.write_with_opc('OUTP:GEN 1')

#Connect power supply to the DUT
root = Tk()
myLabel = Label(root, text= "Please Connect the power supply to the DUT")
myLabel.pack()

myButton = Button(root, text = "Okay!", command = root.destroy)
myButton.pack()
root.mainloop()


znb.write_with_opc("DISPlay:WINDow:TRACe:Y:SCALe:AUTO ONCE, 'Trc1'")
znb.write_with_opc("DISPlay:TRACe:Y:SCALe:PDIVision 0.0500000000000, 'Trc1'")
znb.write_with_opc('INIT:CONT OFF')
znb.write_with_opc('CALC1:MARK1:STAT ON')
time.sleep(3)
nge.write_with_opc('OUTP OFF')


#Close the session
nge.close()
znb.close()
