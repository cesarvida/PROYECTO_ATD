import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 9999

def send_data(source_name, data_dict):
    """
    Sends a dictionary as JSON to the socket server.
    """
    payload = {
        'source': source_name,
        'data': data_dict
    }
    
    try:
        json_str = json.dumps(payload)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json_str.encode('utf-8'))
            response = s.recv(1024)
            print(f"Server response: {response.decode()}")
            if response == b"ACK":
                return True
            else:
                return False
    except Exception as e:
        print(f"Failed to send data to server: {e}")
        return False
