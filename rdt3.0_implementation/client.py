from socket import *
from protocolordt3 import *
file_name = str(input("Digite o nome do seu arquivo: "))


rdt_client = rdt_protocol()
 
try: 
    file = open(file_name,"rb") 
    data = file.read(rdt_client.tam_buffer)
    print (f"Enviando {file_name}")
    while data:
        rdt_client.send_pkg(data)
        data = file.read(rdt_client.tam_buffer)
except FileNotFoundError:
    print("Arquivo não encontrado!")
    exit()
except:
    print("Erro desconhecido")
    exit()



file.close()
file = open("recebidoClient.txt", "wb")

data = rdt_client.receive()

file.write(data)
file.close()

rdt_client.close_connection()
    