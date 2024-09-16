from socketserver import BaseRequestHandler, TCPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            print('got msg: ', msg.decode('utf-8'))
            self.request.send('got it: {}'.format(msg.decode('utf-8')).encode('utf-8'))


if __name__ == '__main__':
    # 定义端口port：20000
    # 这是一种单线程的方式
    serv = TCPServer(('', 20000), EchoHandler)
    print('server started:')
    serv.serve_forever()
