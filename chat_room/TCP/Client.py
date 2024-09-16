from socket import socket, AF_INET, SOCK_STREAM

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 20000))
    s.send('Hello'.encode('utf-8'))
    # 指定接收的端口
    return_msg = s.recv(8192)
    print(return_msg.decode('utf-8'))
