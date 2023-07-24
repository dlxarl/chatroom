import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break

    client_socket.close()

def send_messages(client_socket):
    while True:
        message = input("Введіть ваше повідомлення: ")
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    host = '127.0.0.1'  # Встановіть IP-адресу сервера.
    port = 139  # Встановіть порт сервера.

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    send_thread.join()