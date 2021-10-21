from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


# Setting up constants for later use
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """
    Sets up handling for incoming clients
    """
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greeting from the server!" + "Now type your name and press enter!", "utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):          # Takes client socket as argument
    """
    Handles a single client connection
    """
    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf-8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quite}", "utf-8"):
            broadcast(msg, name + ": ")
        else:
            clients.send(bytes("{quite}", "utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf-8"))
            break


def broadcast(msg, prefix=""):       # Prefix is for identification
    """
    Broadcast the messages to all the clients.
    """
    for client in clients:
        client.send(bytes(prefix, "utf-8") + msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()