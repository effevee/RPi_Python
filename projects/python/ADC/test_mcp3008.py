# uitlezen van een potmeter mbv MCP3008
#
# MCP3008  RPi      POT
# =======================
#  VDD     3V3      
#  Vref    3V3
#  Agnd    GND      
#  SCLK    SPSCLK
#  MISO    SPMISO
#  MOSI    SPMOSI
#  CE      SPICE0
#  Dgnd    GND
# =======================
#  ----    3V3      pin 1
#  CH3     ------   pin 2
#  ----    GND      pin 3
# =======================


from mcp3008 import MCP3008
import time

VCC=3.3   # V

# aanmaken adc object
adc = MCP3008()

try:
    while True:
        # uitlezen channel 3 van MCP3008
        waarde = adc.read(channel=3)
        
        # omrekenen naar spanning
        spanning = waarde / 1023.0 * VCC
        
        # debug info
        print('ADC waarde: %4d - spanning: %.3f Volt'%(waarde, spanning))
        
        # wachten
        time.sleep(1)
        
except KeyboardInterrupt as E:
    print('Programma gestopt met Ctrl-C')
    
finally:
    adc.close()
