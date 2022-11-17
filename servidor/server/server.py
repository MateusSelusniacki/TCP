import socket
import threading

class Server():
    ip = '0.0.0.0'
    all_connections = []
    stop_thread = [0]
    content = ''

    def receive(self,server,connection,address):
        #cria looping de conexão com o cliente
        while(connection in self.all_connections):
            try:
                #aceita conexão
                #recebe dados do cliente e transforma em string
                self.content = connection.recv(8192).decode()
                print(f'{self.content} received from: {address}')
                
            except Exception as E:
                print(f'erro: {E}')
                socket.close()

    def send(self,data):
        for conn in self.all_connections:
            conn.send( data.encode() )

    def listening(self,port):
        #abrindo socket para comunicação TCP/IP
        self.server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

        #fazendo bind do ip e porta
        self.server.bind ( (self.ip,port) )

        #listen
        self.server.listen(1)
        
        while(self.stop_thread[0] != 1):
            try:
                connection, address = self.server.accept()
                print(f'connection receive from: {address}')
                self.all_connections.append(connection)
                threading.Thread(target = self.receive,args = (self.server,connection,address)).start()
            
            except Exception as E:
                print(E)

        self.all_connections = []
        print('fim listening')
        
        self.stop_thread[0] = 0

    def start(self,port):
        print(f'starting server in port {port} ')
        threading.Thread(target = self.listening, args = (port,)).start()

    def stop(self):
        self.server.close()
        self.stop_thread[0] = 1
