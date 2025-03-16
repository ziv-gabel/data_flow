import csv
import sys
from collections import defaultdict

# Check if input file is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

# Get input file from command line argument
input_file = sys.argv[1]
output_file = f"processed_{input_file}"

# Dictionary to store host data
host_data = defaultdict(lambda: {"ip_addresses": set(), "number_of_lines": 0})

# Read the CSV file
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            continue  # Skip malformed lines
        ip, host = row[0].strip(), row[1].strip()
        host_data[host]["ip_addresses"].add(ip)
        host_data[host]["number_of_lines"] += 1

# Write the processed data to a new CSV file
with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["host", "ip_addresses", "number_of_lines"])
    for host, data in host_data.items():
        writer.writerow([host, ", ".join(data["ip_addresses"]), data["number_of_lines"]])

print(f"Processed data saved to {output_file}")

