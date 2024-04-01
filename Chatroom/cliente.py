from pickle import TRUE
import socket
import threading
import random
import datetime


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000,9000)))
canSend = False
firstBanCommand = True
name = ""
lastBanCommand = datetime.datetime.now()


def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

while True:
    message = input("")
    if message == "bye" and canSend:
        client.sendto(message.encode(), ("localhost", 9999))
        exit()
    elif "hi, meu nome eh" in message:
        name = message[15:]
        canSend = TRUE
        client.sendto(message.encode(), ("localhost", 9999))
    elif message[0] == "@" and canSend:
        nameInbox = message[1:message.index(" ")]
        newMessage = f"INBOX/{nameInbox}-" + f"{datetime.datetime.now()} - {name}: {message}"
        client.sendto(newMessage.encode(), ("localhost", 9999))
    elif message == "list" and canSend:
        client.sendto(message.encode(), ("localhost", 9999))
    elif message.startswith("ban") and canSend:
        if firstBanCommand:
            firstBanCommand = False
            lastBanCommand = datetime.datetime.now()
            client.sendto(message.encode(), ("localhost", 9999))
        else:
            if (datetime.datetime.now() - lastBanCommand).total_seconds() > 60:
                lastBanCommand = datetime.datetime.now()
                client.sendto(message.encode(), ("localhost", 9999))
            else:
                print("Você só pode executar um comando de ban a cada 60 segundos!")
    elif canSend:
        client.sendto(f"{datetime.datetime.now()} - {name}: {message}".encode(), ("localhost", 9999))
    else:
        print("É necessário se conectar à sala para enviar mensagens")