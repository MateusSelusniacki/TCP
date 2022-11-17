import socket
import threading

class Client():
    content = ''

    def receive(self):
        self.content = self.client.recv(8192).decode()
        threading.Thread(target = self.receive).start()
    
    def connect(self,ip,port):
        try:
            self.client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.conn = self.client.connect( ( ip, port ) )
            threading.Thread(target = self.receive).start()
        
            return 1
        except Exception as E:
            print(E)
            return 0

    def disconnect(self):   
        try:
            self.client.close()
        except Exception as E:
            print(E)
            return

    def send(self,data):
        self.client.send(data.encode())