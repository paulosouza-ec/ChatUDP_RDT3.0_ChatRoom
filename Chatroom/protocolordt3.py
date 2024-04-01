from socket import *

localhost="127.0.0.1"
porta=5005
default_time = 20





class rdt_protocol:

    ################# CONFIGURACOES INICIAIS PARA CLASSE #############################

    def __init__(self, flag_server = 0, addressPort = (localhost, porta), tam_buffer = 1024): #constructor
        #setando valores dos atributos como portas, tam do buffer, endereço de destinatario, configuracao do socket UDP
        self.tam_buffer = tam_buffer
        self.end_envio = 0
        self.addressPort =  addressPort
        self.UDPSocket = socket(AF_INET, SOCK_DGRAM)
        self.flag_server = flag_server
        self.n_seq = 0
        if flag_server == True: #1 server 0 client ... Detecta se se trata do cliente ou servidor
            self.UDPSocket.bind(self.addressPort)
            self.UDPSocket.settimeout(2.0)
            print("SERVIDOR ON")
        else:
            print("CLIENTE ON")
    # Métodos da classe

    
    def define_cabecalho(self, data): #Cria o cabecalho (Funcao auxiliar de send_pkg)

        chcksum = checksum(data)

        return str({
            'seq': self.n_seq,
            'checksum': chcksum,
            'payload' : data
        }).encode()

    
    def checksum_(self, chcksum, payload):  #Checagem checksum recept e sender
        if checksum(payload) == chcksum:
            return True
        else:
            return False
    
    def nseq_update(self): #apenas para realizar o update do numero de sequencia
        return  (1 - self.n_seq)


    def send(self, data): # transm Envia dado via socket udp para o cliente ou servidor (Funcao auxiliar de send_pkg)
        if self.flag_server:
            self.UDPSocket.sendto(data, self.end_envio)
        else:
            self.UDPSocket.sendto(data, self.addressPort)

    def send_pkg(self, data): 
        data = self.define_cabecalho(data.decode())
        ack = False

        while not ack: #envio de dado atraves de conexao udp
            self.send(data)

            try:
                data, self.end_envio = self.UDPSocket.recvfrom(self.tam_buffer)
            except socket.timeout: #Estouro do temporizador
                print("O ACK PRECISA SER REENVIADO") 
            else: 
                ack = self.rcv_ack(data)

    def receive(self): #Recebimento do dado cliente ou server
        print("...RECEBENDO PACOTE...")
        self.UDPSocket.settimeout(default_time) 
        data, self.end_envio = self.UDPSocket.recvfrom(self.tam_buffer)
        data = self.rcv_pkg(data)

        if data != "":   #Caso nao haja  mais arquivos a ser passado para variavel temporaria que armazena de 1024 a 1024 bytes
            buffer = data
        print("PACOTE RECEBIDO POR COMPLETO")
        return buffer.encode()

    def send_ack(self, ack): #envio de recomhecimento de pacote
        if ack:
            data = self.define_cabecalho("ACK")
        else:
            data = self.define_cabecalho("NACK")
        self.send(data)

    def rcv_pkg(self, data):
        data = eval(data.decode())
        n_seq = data['seq']
        checksum = data['checksum']
        payload = data['payload']

        if self.checksum_(checksum, payload) and n_seq == self.n_seq:
            self.send_ack(1)
            self.n_seq = self.nseq_update()
            return payload
        else:
            self.send_ack(0)
            return ""


    def rcv_ack(self, data): #Checagem de reconhecimento de pacote 
        data = eval(data.decode())
        n_seq = data['seq']
        checksum = data['checksum']
        payload = data['payload']

        if self.checksum_(checksum, payload) and n_seq == self.n_seq and payload == "ACK": #Caso esperado (Sem problema nhm)
            self.n_seq = self.nseq_update()
            return True #ACK
        else:
            return False #NACK

    def close_connection(self): #Encerramento de conexao
        self.UDPSocket.close()

def checksum(data): #Calculo do checksum
        sum = 0
        for i in range(0,len(data),2):
            if i + 1 >= len(data):
                sum += ord(data[i]) & 0xFF
            else:
                w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
                sum += w
    # Extrai 16 dos 32 bits soma e add os carries
        while (sum >> 16) > 0:
            sum = (sum & 0xFFFF) + (sum >> 16)
        sum = ~sum
        return sum & 0xFFFF



print("...PROTOCOLO RDT3.0 ATIVADO...\n - PRONTO PARA FAZER A TRANSFERÊNCIA CONFIÁVEL! -")


