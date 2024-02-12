from socket import *
import threading
serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

username = input("Choose your username! ")

def receive():
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                clientSocket.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occured!")
            clientSocket.close()
            break

def write():
    while True:
        message = f'{username}: {input("")}'
        clientSocket.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()