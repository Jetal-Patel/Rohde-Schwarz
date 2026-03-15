"""This is an example script to emulate the HP8753 VNA with the R&S ZNB
"""


import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
_8753es = rm.open_resource('TCPIP::100.100.100.11::hislip0')
#_8753es.write('SYSTem:LOGGing:REMote:STATe ON') # May sometimes be needed
idn = _8753es.query('*IDN?')
print(f"\nHello, I am: '{idn}'")

# HP 8753A Commands to Measure Bandpass Filter
_8753es.write('*RST')
_8753es.write('STAR 350MHZ') # Start Frequency
_8753es.write('STOP 500MHZ') # Stop Frequency
_8753es.write('CHAN1') # Channel 1
_8753es.write('S21') # Measure S21
_8753es.write('LOGM') # Format Log Magnitude
_8753es.write('CHAN2') # Channel 2
_8753es.write('S21') # Measure S21
_8753es.write('PHAS') # Format Phase
_8753es.write('CHAN3') # Channel 3
_8753es.write('S11') # Measure S11
_8753es.write('SMIC') # Format Smith
_8753es.write('CHAN4') # Channel 4
_8753es.write('MEASA') # Measure reflected power
_8753es.write('LOGM') # Format Log Magnitude
_8753es.write('SPLID4') # Show 4 separate traces

# Prompt User to Connect DUT
input("Please connect the DUT and then press ENTER to continue...")

# Autoscale the Channels
_8753es.write('CHAN1 AUTO') # Autoscale Channel 1
_8753es.write('MARK1 433MHZ') # Place Marker1 on Channel 1 at 433MHz
_8753es.write('CHAN2 AUTO') # Autoscale Channel 2
_8753es.write('CHAN3 AUTO') # Autoscale Channel 3
_8753es.write('CHAN4 AUTO') # Autoscale Channel 4
_8753es.write('MARKCOUP') # Coupled Markers

# Close the session
_8753es.close()
