"""
lcd_test.py - Quick test script for an LCD1602 with an I2C (PCF8574) backpack.

Wiring (backpack -> Pi):
    GND -> GND
    VCC -> 5V
    SDA -> SDA1 (GPIO2, physical pin 3)
    SCL -> SCL1 (GPIO3, physical pin 5)

One-time setup before running:
    1. Enable I2C: sudo raspi-config -> Interface Options -> I2C -> Enable, then reboot.
    2. Install dependencies:
         sudo apt install python3-smbus i2c-tools
         pip install RPLCD
    3. Find your LCD's I2C address:
         sudo i2cdetect -y 1
       It'll show up as a two-digit hex address in the grid, commonly 0x27 or 0x3F.
       Update I2C_ADDRESS below to match what you see.
"""

import time
from RPLCD.i2c import CharLCD

I2C_ADDRESS = 0x27  # change this if i2cdetect shows a different address
I2C_PORT = 1        # 1 on every Pi with a 40-pin header, Pi Zero included


def main():
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=I2C_ADDRESS,
        port=I2C_PORT,
        cols=16,
        rows=2,
        dotsize=8,
        charmap='A02',
        auto_linebreaks=True,
    )

    # Basic text test
    lcd.clear()
    lcd.write_string('Hello, Roger!')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('LCD1602 online')
    time.sleep(3)

    # Fill both rows to check every character position is wired and lit correctly
    lcd.clear()
    lcd.write_string('0123456789ABCDEF')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('FEDCBA9876543210')
    time.sleep(3)

    # Backlight toggle test
    for _ in range(4):
        lcd.backlight_enabled = False
        time.sleep(0.3)
        lcd.backlight_enabled = True
        time.sleep(0.3)

    lcd.clear()
    lcd.write_string('Test complete')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')