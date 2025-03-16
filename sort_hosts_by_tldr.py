import sys
from tldextract import extract

# Check if a filename was provided
if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# Read the list of hosts from the file
try:
    with open(filename, "r") as file:
        hosts = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)

# Sort by the base domain (TLD + SLD)
sorted_hosts = sorted(hosts, key=lambda host: (extract(host).registered_domain, host))

# Print sorted list
for host in sorted_hosts:
    print(host)
