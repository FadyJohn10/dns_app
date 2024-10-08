from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request: Missing parameters", 400

    dns_query = f"TYPE=A\nNAME={hostname}\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(dns_query.encode(), (as_ip, int(as_port)))
        data, _ = s.recvfrom(1024)
    
    dns_response = data.decode().split('\n')
    fs_ip = dns_response[2].split('=')[1]

    fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    response = requests.get(fs_url)

    if response.status_code == 200:
        return jsonify({"fibonacci": response.json()}), 200
    else:
        return "Error from Fibonacci Server", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)