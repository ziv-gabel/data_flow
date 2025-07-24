# Check if a file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <file.pcapng>"
    exit 1
fi

PCAP_FILE="$1"

# Check if the file exists
if [ ! -f "${PCAP_FILE}" ]; then
    echo "Error: File '${PCAP_FILE}' not found!"
    exit 1
fi

# Define output filenames
RESOLVED_ADDRESSES_FILE="${PCAP_FILE%.*}_resolved_addresses.txt"
ENDPOINTS_FILE="${PCAP_FILE%.*}_endpoints.txt"

# Extract resolved addresses
tshark -r "$PCAP_FILE" -q -z hosts > ${RESOLVED_ADDRESSES_FILE}
tail -n +5 ${RESOLVED_ADDRESSES_FILE} > temp.txt && mv temp.txt ${RESOLVED_ADDRESSES_FILE}
sed -i '' '/^192\.168.*\.local$/d' ${RESOLVED_ADDRESSES_FILE}
sed -i '' 's/\t/,/g' ${RESOLVED_ADDRESSES_FILE}
echo "Resolved addresses saved to: ${RESOLVED_ADDRESSES_FILE}"

# Extract endpoints
tshark -r "$PCAP_FILE" -q -z endpoints,ip > ${ENDPOINTS_FILE}
sed '1,4d' ${ENDPOINTS_FILE} | sed -e :a -e '$d;N;2,2ba' -e 'P;D' > temp.txt && mv temp.txt ${ENDPOINTS_FILE}
sed -E -i '' 's/ +/ /g' ${ENDPOINTS_FILE}
echo "Endpoints saved to: ${ENDPOINTS_FILE}"

 python3 process_resolved.py ${RESOLVED_ADDRESSES_FILE}
 python3 aggregate_traffic.py processed_${RESOLVED_ADDRESSES_FILE} ${ENDPOINTS_FILE}


echo "Extraction completed."