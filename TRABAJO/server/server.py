import socket
import json
import os
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 9999
# Asegurar que los datos se guarden en TRABAJO/data sin importar desde dónde se ejecute
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '../data/raw_data.jsonl')

def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    try:
        data = conn.recv(1024 * 1024) # 1MB max
        if not data:
            return
        
        # Descodificar mensaje
        message = data.decode('utf-8')
        print(f"Datos recibidos: {message[:100]}...")
        
        # Parsear JSON para validar que esté bien formado
        json_data = json.loads(message)
        
        # Añadir timestamp de recepción
        json_data['_received_at'] = datetime.now().isoformat()
        
        # Guardar en fichero (thread safe-ish para append en linux)
        with open(DATA_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(json_data) + '\n')
            
        conn.sendall(b"ACK")
    except Exception as e:
        print(f"Error gestionando cliente: {e}")
        conn.sendall(b"ERR")
    finally:
        conn.close()

def start_server():
    # Asegurar que el directorio de datos existe
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            # Gestionar en un hilo para permitir múltiples scrapers a la vez
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    start_server()
