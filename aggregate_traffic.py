import csv
import sys
from collections import defaultdict

# Check if input files are provided
if len(sys.argv) < 3:
    print("Usage: python script.py <processed_hosts_file> <traffic_data_file>")
    sys.exit(1)

# Get input file names
processed_hosts_file = sys.argv[1]
traffic_data_file = sys.argv[2]

# Dictionary to map IPs to hosts and store number of occurrences
ip_to_host = {}
host_occurrences = {}

# Read the processed hosts file
with open(processed_hosts_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        if len(row) < 3:
            continue
        host = row[0].strip()
        ips = row[1].split(", ")  # List of IPs
        occurrences = int(row[2])  # Number of times the host appeared
        
        host_occurrences[host] = occurrences
        for ip in ips:
            ip_to_host[ip] = host

# Dictionary to store aggregated traffic data per host
host_traffic = defaultdict(lambda: {"packets": 0, "bytes": 0})

# Read the traffic data file
with open(traffic_data_file, newline='', encoding='utf-8') as file:
    for line in file:
        parts = line.split()
        if len(parts) < 3:
            continue
        ip = parts[0].strip()
        packets = int(parts[1])
        bytes_transferred = int(parts[2])
        
        if ip in ip_to_host:
            host = ip_to_host[ip]
            host_traffic[host]["packets"] += packets
            host_traffic[host]["bytes"] += bytes_transferred

# Output aggregated results
output_file = f"aggregated_{processed_hosts_file}"
with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["host", "number_of_lines", "total_packets", "total_bytes"])
    for host, data in host_traffic.items():
        occurrences = host_occurrences.get(host, 0)
        writer.writerow([host, occurrences, data["packets"], data["bytes"]])

print(f"Aggregated traffic data saved to {output_file}")
