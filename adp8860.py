# import the needed packages
import smbus
import sys
import os
import time

# create a varible to handle the bus
try:
    bus = smbus.SMBus(1)
except IOError:
    print("SMBus error")
    sys.exit(1)

# constants
DEVICE_ADDR_7_BITS = 0x2A
MFDVID = 0x00 # Manufacture + Device ID
MDCR = 0x01 # Mode Control Register
BLSEN = 0x05 # Backlist Sink Enable
ISCC = 0x10 # Independent Sink Current Control
ISCT1 = 0x11 # Independent Sink Current Time
ISCT2 = 0x12 # Independent Sink Current Time
ISCF = 0x13 # Independent Sink Current Fade
LED7_CURRENT = 0x14 # 0x15, 0x16, ... 0x1A for the other LEDs (6, 5, ..., 1)

mfdvid = bus.read_byte_data(DEVICE_ADDR_7_BITS, MFDVID)
sys.stdout.write('Manufacture + Device ID : %d\n' % (mfdvid))
time.sleep(0.05)

bus.write_byte_data(DEVICE_ADDR_7_BITS, MDCR, 0x20)
time.sleep(0.05)

bus.write_byte_data(DEVICE_ADDR_7_BITS, BLSEN, 0x7F)
time.sleep(0.05)

for currentRegister in range(LED7_CURRENT, LED7_CURRENT + 7):
    bus.write_byte_data(DEVICE_ADDR_7_BITS, currentRegister, 0x7F) # 30 mA for all channels
    time.sleep(0.05)

bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCC, 0x7F) # enable all channels
time.sleep(0.05)

#bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCT1, 0xFF)
bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCT1, 0x00)
time.sleep(0.05)

#bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCT2, 0xFF)
bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCT2, 0x00)
time.sleep(0.05)

#bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCF, 0x33)
bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCF, 0x00)
time.sleep(0.05)

while True:
    try:
        bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCC, 0x7F) # enable all channels
        time.sleep(1)
        
        bus.write_byte_data(DEVICE_ADDR_7_BITS, ISCC, 0x00) # disable all channels
        time.sleep(1)
        
    except KeyboardInterrupt:
        bus.write_byte_data(DEVICE_ADDR_7_BITS, MDCR, 0x00)
        sys.exit(0)
        
    except IOError:
        print("Disconnected")
        sys.exit(1)