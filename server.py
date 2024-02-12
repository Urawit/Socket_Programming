from socket import *
import threading

STATUS_USERNAME_APPENDED = 100
STATUS_CONNECTED_TO_SERVER = 200
STATUS_CONNECTED_TO_CLIENT = 202
STATUS_DISCONNECTED_FROM_SERVER = 204
STATUS_SENT = 300
STATUS_QUIT = 404

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print('The server is ready to receive!\n')

# Maintain a list of client sockets
client_sockets = []
usernames = []

def broadcast(message):
    for client in client_sockets:
        client.send(message)

# Function to handle each client's connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == '\x03':  # Ctrl+C signal
                raise KeyboardInterrupt
            if not message:  # Client disconnected
                raise ConnectionError
            message = "(" + str(STATUS_SENT) + ") " + message
            broadcast(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("(" + str(STATUS_DISCONNECTED_FROM_SERVER) + ") " + "Client disconnected")
            break
        except ConnectionError:
            print("(" + str(STATUS_DISCONNECTED_FROM_SERVER) + ") " + "Client disconnected")
            break
        except Exception as e:
            print("An error occurred:", e)
            break
    # Client disconnected, perform cleanup
    index = client_sockets.index(client)
    client_sockets.remove(client)
    client.close()
    username = usernames[index]
    message = "(" + str(STATUS_QUIT) + ") " + f'{username} left the chat!'
    broadcast(message.encode('utf-8'))
    usernames.remove(username)

def receive():
     while True:
        client, addr = serverSocket.accept()
        response = "(" + str(STATUS_CONNECTED_TO_CLIENT) + ") " + f'connected with {str(addr)}`'
        print(response)

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        client_sockets.append(client)
        
        user_appended_response = "(" + str(STATUS_USERNAME_APPENDED) + ") " + f"Username of the client is {username}!"
        print(user_appended_response)
        broadcast(f'{username} joined the chat!'.encode('utf-8'))
        conected_to_server_response = "(" + str(STATUS_CONNECTED_TO_SERVER) + ") " + 'Conected to the server!'
        client.send(conected_to_server_response.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
