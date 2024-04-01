import socket
import threading
import queue

messages = queue.Queue()
clients = {}
countBans = {}
banTable = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost",9999))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if "hi, meu nome eh" in message.decode(): 
                if addr not in banTable:
                    name = message.decode()[15:]
                    if addr not in clients.keys():
                        clients[addr] = name
                    for client in clients.keys():
                        server.sendto(f"{name} entrou na sala!".encode(), client)
            elif message.decode() == "list":
                if addr not in banTable:
                    for client in clients.keys():
                        server.sendto(f"{clients[client]}".encode(), addr)
            elif message.decode().startswith("INBOX"):
                if addr not in banTable:
                    name = message.decode()[message.decode().index("/")+1:message.decode().index("-")]
                    for client in clients.keys():
                        if name.strip() == clients[client].strip():
                            p = message.decode().index("-")
                            server.sendto(f"{message.decode()[p+1:]}".encode(), client)
            elif message.decode().startswith("ban"):
                if addr not in banTable:
                    name = message.decode()[message.decode().index("@")+1:]
                    for client in clients.keys():
                        if clients[client].strip() == name.strip():
                            if client not in countBans:
                                countBans[client] = 1
                            else:
                                (countBans[client]) = countBans[client] + 1
                                if countBans[client] >= ((2/3) * len(clients)):
                                    banTable.append(client)
                                    countBans.pop(client)
                                    for c in clients.keys():
                                        server.sendto(f"{clients[client]} foi banido da sala!".encode(), c)
                    for client in banTable:
                        if client in clients.keys():
                            clients.pop(client)

            elif message.decode() == "bye":
                for client in clients.keys():
                        server.sendto(f"{clients[addr]} saiu da sala!".encode(), client)
                clients.pop(addr)
            else:
                for client in clients.keys():
                    try:
                        if addr not in banTable and addr != client:
                                server.sendto(message, client)
                    except:
                        del clients[client]

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

                