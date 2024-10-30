import time
import csv
import random

# Function to get the current time in "HH:MM" format
def get_current_time():
    return time.strftime("%H:%M")

# Generate some random numerical data
random_data = random.randint(1, 100)

# File path for the CSV file
csv_file = "output.csv"

# Open the CSV file in append mode
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write the current time and random data into the CSV
    writer.writerow([get_current_time(), random_data])

print(f"Data written to {csv_file}")
