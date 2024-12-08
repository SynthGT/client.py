import socket
from cryptography.fernet import Fernet
import threading

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

# Receive encryption key from server
encryption_key = client.recv(1024)
cipher = Fernet(encryption_key)

def receive_messages():
    while True:
        try:
            message = client.recv(1024)
            print(cipher.decrypt(message).decode())
        except:
            print("[ERROR] Connection lost.")
            client.close()
            break

def send_messages():
    username = input("Enter your username: ")
    client.send(cipher.encrypt(username.encode()))
    print("Connected to the chat.")

    while True:
        message = input()
        client.send(cipher.encrypt(message.encode()))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()
