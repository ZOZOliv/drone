import serial, time

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    #with serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1) as arduino: #Linux
    with serial.Serial(port="COM3", baudrate=9600, timeout=1) as arduino: #Windows
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    cmd = input("Enter command (CMD:255,255,255,255): ")
                    arduino.write(cmd.encode())
                    #time.sleep(0.1) #wait for arduino to answer
                    
                    while arduino.inWaiting() == 0: 
                        pass
                    
                    if arduino.inWaiting() > 0: 
                        answer = str(arduino.readline())
                        print("---> {}".format(answer))                            
                        arduino.flushInput() #remove data after reading
                            
            except KeyboardInterrupt:
                arduino.close()
                print("KeyboardInterrupt has been caught.")
