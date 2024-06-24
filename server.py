import socket
import threading


host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
        

def receive():
    while True:
        client, addr = server.accept()
        #print(f"$$$ {client} connected to the server")
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"{nickname} joined the room.")
        client.send(f"Connected to the server".encode('utf-8'))
        broadcast(f"{nickname} joined the chat".encode('utf-8'))
        
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        

def handle(client):
    while True:
        try: 
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat".encode('utf-8'))
            break

        
        
if __name__ == "__main__":
    print("Server is ready for getting clients. Listening.........")
    receive()
        
    