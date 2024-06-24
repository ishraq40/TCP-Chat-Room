import socket
import threading

nickname = input("Enter nickname to join the chat: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message=="NICK":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('An error occurred')
            client.close()
            break


def write():
    while True:
        text = input('')
        message = f">>{nickname}: {text} ".encode('utf-8')
        client.send(message)
       
       
if __name__ == "__main__":    
    receiving_thread = threading.Thread(target=receive)
    receiving_thread.start()
    
    send_thread = threading.Thread(target=write)
    send_thread.start()