import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            print(f'收到消息: {message}')
        except:
            print('与服务器断开连接')
            client.close()
            break

def send_message():
    while True:
        message = input('请输入消息: ')
        data = json.dumps({'message': message})
        client.send(data.encode('utf-8'))

def request_peer_connection(peer_addr):
    data = json.dumps({'action': 'connect', 'peer_addr': peer_addr})
    client.send(data.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_message)

receive_thread.start()
send_thread.start()

while True:
    peer_addr = input('请输入要聊天的对方地址 (格式: ip:port): ')
    request_peer_connection(peer_addr)
