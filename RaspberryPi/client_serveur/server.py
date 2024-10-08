import socket               # Import socket module
import threading
import queue
import time

q_cmd = queue.Queue()

client_event = threading.Event()

def on_new_client(clientsocket, addr):
    print('Got connection from', addr)
    client_event.set()
    while True:
        if not q_cmd.empty():
            cmd = q_cmd.get()
            clientsocket.send(cmd.encode())
            print(addr, ' << ', cmd)

        try:
            msg = clientsocket.recv(1024).decode()
            if msg == '':
                print('Fermeture connexion', addr)
                clientsocket.close()
                break

            #do some checks and if msg == someWeirdSignal: break:
            print(addr, ' >> ', msg)
        except Exception as e:
            print('Fermeture connexion', addr)
            clientsocket.close()
            break
    client_event.clear()

def send_cmd():
    while True:
        if client_event.is_set():
            q_cmd.put('CMD:255,255,255,255')
            time.sleep(10)
        else:
            q_cmd.queue.clear()
            time.sleep(0.5)

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 5000                 # Reserve a port for your service.

print('Server started!')
print('Waiting for clients...')

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

threadCmd = threading.Thread(target=send_cmd, daemon=True)
threadCmd.start()

try:
    while True:
        c, addr = s.accept()     # Establish connection with client.
        threadSocket = threading.Thread(target=on_new_client, args=(c,addr), daemon=True)
        threadSocket.start()
        Connected = True

except KeyboardInterrupt:
    s.close()
    print("Arrêt du programme")
