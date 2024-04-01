from socket import *
from protocolordt3 import *

rdt_server = rdt_protocol(1)
data = rdt_server.receive()
file = open("recebidoServer.txt",'wb')
file.write(data)
file.close()

file = open("recebidoServer.txt","rb") 
data = file.read(rdt_server.tam_buffer)

while data:
    rdt_server.send_pkg(data)
    data = file.read(rdt_server.tam_buffer)

rdt_server.close_connection()
file.close()





