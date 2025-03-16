# Check if a file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file.pcapng>"
    exit 1
fi

PCAP_FILE="$1"

# Check if the file exists
if [ ! -f "$PCAP_FILE" ]; then
    echo "Error: File '$PCAP_FILE' not found!"
    exit 1
fi

# Define output filenames
RESOLVED_ADDRESSES_FILE="${PCAP_FILE%.*}_resolved_addresses.txt"
ENDPOINTS_FILE="${PCAP_FILE%.*}_endpoints.txt"

# Extract resolved addresses
tshark -r "$PCAP_FILE" -q -z hosts > "$RESOLVED_ADDRESSES_FILE"
echo "Resolved addresses saved to: $RESOLVED_ADDRESSES_FILE"

# Extract endpoints
tshark -r "$PCAP_FILE" -q -z endpoints,ip > "$ENDPOINTS_FILE"
echo "Endpoints saved to: $ENDPOINTS_FILE"

echo "Extraction completed."