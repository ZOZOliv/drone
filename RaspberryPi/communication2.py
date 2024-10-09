import threading
import queue
import serial
import time
import socket


q_cmd = queue.Queue()
q_read = queue.Queue()

stop_event = threading.Event()

def com_arduino():
    #port = "/dev/ttyACM0"
    port = "COM5"
    connected = False
    while True:
        if not connected:
            try:
                print("{} connexion...".format(port))
                arduino = serial.Serial(port=port, baudrate=9600, timeout=1)
                time.sleep(0.1) #wait for serial to open
                if arduino.isOpen():
                    print("{} connecté !".format(arduino.port))
                    connected = True
                else:
                    connected = False
            except Exception as e:
                connected = False
                time.sleep(2)
        else:
            if not q_cmd.empty():
                cmd = q_cmd.get()
                print("Write ---> {}".format(cmd))    
                arduino.write(cmd.encode())
                while arduino.out_waiting > 0:
                    time.sleep(0.2)
            
            while arduino.in_waiting > 0:
                answer = arduino.readline().decode().replace('\r\n', '') 
                #answer = str(arduino.readline())
                q_read.put(answer)
                print("Read ---> {}".format(answer))                            
                arduino.flushInput() #remove data after reading

        if stop_event.is_set():
                if connected:
                    arduino.close()
                print("{} déconnecté...".format(port))
                break

def com_socket():
    #host = socket.gethostname()  # as both code is running on same pc
    host = 
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    connected = False
    
    while True:
        if not connected:
            try:
                print("{} connexion...".format(host))
                client_socket.connect((host, port))  # connect to the server
                client_socket.setblocking(False)
                connected = True
            except Exception as e:
                connected = False
                time.sleep(1)
        else:
            if not q_read.empty():
                read = q_read.get()
                client_socket.send(read.encode())  # send message
            else:
                try:
                    data = client_socket.recv(1024).decode()  # receive response
                    q_cmd.put(data)
                except BlockingIOError as e:
                    pass
        
        if stop_event.is_set():
            if connected:
                client_socket.close()  # close the connection
            print("{} déconnecté...".format(host))
            break

threadArduino = threading.Thread(target=com_arduino, daemon=True)
threadArduino.start()

threadSocket = threading.Thread(target=com_socket, daemon=True)
threadSocket.start()


try:
    while True:
        time.sleep(2)

except KeyboardInterrupt:
    stop_event.set()
    threadArduino.join()
    threadSocket.join()
    print("Arrêt du programme")
