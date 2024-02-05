import serial
from datetime import datetime
import psycopg2
import tkinter as tk
from tkinter import simpledialog

arduino_port = 'COM4'
baud_rate = 9600

# PostgreSQL connection parameters
db_params = {
    'dbname': '************',
    'user': '************',
    'password': '************',
    'host': '************',
    'port': '************'
}

# Function to get the table name using tkinter dialog
def get_table_name():
    root = tk.Tk()
    root.withdraw()
    table_name = simpledialog.askstring("Table Name", "Enter the table name:")
    return table_name

def create_table(cursor, table_name):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ecg FLOAT,
            x FLOAT,
            y FLOAT,
            z FLOAT,
            timestamp TIMESTAMP
        );
    """)

def insert_data(cursor, ecg, x, y, z, timestamp, table_name):
    cursor.execute(f"""
        INSERT INTO {table_name} (ecg, x, y, z, timestamp)
        VALUES (%s, %s, %s, %s, %s);
    """, (ecg, x, y, z, timestamp))

def read_sensor_data(cursor, table_name):
    try:
        while True:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    data = line.split()
                    ecg, x, y, z = float(data[1]), float(data[3]), float(data[5]), float(data[7])
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                    insert_data(cursor, ecg, x, y, z, timestamp, table_name)

                    print(f"ECG: {ecg} X: {x}  Y: {y}  Z: {z}  Timestamp: {timestamp}")
            except IndexError:
                pass
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        # Get the table name from the user
        table_name = get_table_name()

        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        create_table(cursor, table_name)

        # Open the serial port
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)

        # Read sensor data and insert into PostgreSQL
        read_sensor_data(cursor, table_name)

    except serial.SerialException:
        print(f"Error: Unable to open serial port {arduino_port}. Make sure it's the correct port.")
    finally:
        # Close the serial port and database connection
        ser.close()
        connection.commit()
        cursor.close()
        connection.close()
