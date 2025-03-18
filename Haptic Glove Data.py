import serial
import csv
import time

# Set up Serial connection (check your Arduino COM port)
ser = serial.Serial('COM5', 115200)  # Change 'COM4' to your actual port (Mac/Linux: '/dev/ttyUSB0')

# Open CSV file
filename = "sensor_data.csv"
with open(filename, "w", newline='') as file:
    writer = csv.writer(file)

    # Wait for Arduino to send data
    time.sleep(2)

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line and not line.startswith("Setup"):  # Skip non-data lines
                writer.writerow(line.split(","))  # Write to CSV
                print(line)  # Optional: Print to terminal
        except KeyboardInterrupt:
            print("Stopping Data Logging.")
            break

ser.close()

