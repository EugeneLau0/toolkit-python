import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
client_pairs = {}

def handle_client(client_socket, addr):
    print(f'新连接: {addr}')
    clients[addr] = client_socket
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            print(f'收到来自 {addr} 的消息: {message}')
            if message['action'] == 'connect':
                peer_addr = message['peer_addr']
                if peer_addr in clients:
                    peer_socket = clients[peer_addr]
                    client_pairs[addr] = peer_addr
                    peer_pairs[peer_addr] = addr
                    client_socket.send(json.dumps({'status': 'connected'}).encode('utf-8'))
                    peer_socket.send(json.dumps({'status': 'connected'}).encode('utf-8'))
                else:
                    client_socket.send(json.dumps({'status': 'peer_not_found'}).encode('utf-8'))
            elif addr in client_pairs:
                recipient_addr = client_pairs[addr]
                recipient_socket = clients[recipient_addr]
                recipient_socket.send(json.dumps(message).encode('utf-8'))
    finally:
        print(f'断开连接: {addr}')
        del clients[addr]
        if addr in client_pairs:
            del client_pairs[addr]
            other_addr = client_pairs.get(recipient_addr)
            if other_addr:
                del client_pairs[other_addr]
        client_socket.close()

while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
