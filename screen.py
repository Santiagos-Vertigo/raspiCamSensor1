#!/usr/bin/python3

import subprocess

def main():
    try:
        # Execute the i2cdetect command
        result = subprocess.run(['i2cdetect', '-y', '1'], stdout=subprocess.PIPE)
        # Print the output of the command
        print(result.stdout.decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

