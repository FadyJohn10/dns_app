import socket
import json

DNS_FILE = 'dns_records.json'

def load_dns_records():
    try:
        with open(DNS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_dns_records(records):
    with open(DNS_FILE, 'w') as f:
        json.dump(records, f)

def handle_registration(data):
    lines = data.split('\n')
    record = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=')
            record[key] = value
    
    dns_records = load_dns_records()
    dns_records[record['NAME']] = record
    save_dns_records(dns_records)

def handle_query(data):
    lines = data.split('\n')
    query = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=')
            query[key] = value
    
    dns_records = load_dns_records()
    if query['NAME'] in dns_records:
        record = dns_records[query['NAME']]
        return f"TYPE={record['TYPE']}\nNAME={record['NAME']}\nVALUE={record['VALUE']}\nTTL={record['TTL']}\n"
    else:
        return "Error: Record not found"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))

    print("Authoritative Server is running...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        data = data.decode()

        if data.startswith("TYPE=A\nNAME="):
            if "\nVALUE=" in data:
                handle_registration(data)
                server_socket.sendto("Registration successful".encode(), addr)
            else:
                response = handle_query(data)
                server_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    main()