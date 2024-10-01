import threading
import queue
import serial
import time

q_cmd = queue.Queue()
stop_event = threading.Event()

def com_arduino():
    #with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1) as arduino: #Linux
    with serial.Serial(port="COM3", baudrate=9600, timeout=1) as arduino: #Windows
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connecté !".format(arduino.port))
            while True:
                if not q_cmd.empty():
                    cmd = q_cmd.get()
                    arduino.write(cmd.encode())
                    while arduino.out_waiting > 0: 
                        time.sleep(0.2)

                
                while arduino.in_waiting > 0: 
                    answer = str(arduino.readline())
                    print("---> {}".format(answer))                            
                    arduino.flushInput() #remove data after reading

                if stop_event.is_set():
                    arduino.close()
                    print("{} déconnecté...".format(arduino.port))
                    break


thread = threading.Thread(target=com_arduino, daemon=True)
thread.start()

try:
    while True:
        cmd = input("Enter command (CMD:255,255,255,255): ")
        #cmd = "CMD:255,255,255,255"
        q_cmd.put(cmd)
        time.sleep(2)

except KeyboardInterrupt:
    stop_event.set()
    thread.join()
    print("Arrêt du programme")
