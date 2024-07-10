#!/usr/bin/python3

import smbus

# Create an instance of the SMBus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# Address of the I2C device
DEVICE_ADDRESS = 0x27  # The detected I2C address

# Function to read a byte from a specific register
def read_byte(register):
    try:
        data = bus.read_byte_data(DEVICE_ADDRESS, register)
        print(f"Data read from register {register}: {data}")
    except Exception as e:
        print(f"Error reading from register {register}: {e}")

# Function to write a byte to a specific register
def write_byte(register, value):
    try:
        bus.write_byte_data(DEVICE_ADDRESS, register, value)
        print(f"Wrote {value} to register {register}")
    except Exception as e:
        print(f"Error writing to register {register}: {e}")

# Main function to demonstrate reading and writing
def main():
    # Example: Reading data from register 0x00
    register_to_read = 0x00  # Replace with the register you want to read from
    read_byte(register_to_read)
    
    # Example: Writing data to register 0x00
    register_to_write = 0x00  # Replace with the register you want to write to
    value_to_write = 0x01  # Replace with the value you want to write
    write_byte(register_to_write, value_to_write)

if __name__ == "__main__":
    main()

