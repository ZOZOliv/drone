String msg = ""; // CMD:10,-10,-10,0

int gaz;      //  0/100
int posX;     // -100/100
int posY;     // -100/100
int rotation; // -1/0/1

void setup() {
    Serial.begin(9600);
}

void loop() {
    readSerialPort();
    if (msg.startsWith("CMD")) {
        decodeCmd(msg);
        sendAck();
    }
    else {
        sendData();
    }
    delay(500);
}

void decodeCmd(String cmd) {
    int tempStart = 0;
    int tempEnd = 0;

    tempStart = cmd.indexOf(':') + 1;
    tempEnd = cmd.indexOf(',', tempStart);
    gaz = cmd.substring(tempStart, tempEnd).toInt();

    tempStart = tempEnd + 1;
    tempEnd = cmd.indexOf(',', tempStart);
    posX = cmd.substring(tempStart, tempEnd).toInt();

    tempStart = tempEnd + 1;
    tempEnd = cmd.indexOf(',', tempStart);
    posY = cmd.substring(tempStart, tempEnd).toInt();

    tempStart = tempEnd + 1;
    rotation = cmd.substring(tempStart).toInt();
}

void readSerialPort() {
    msg = "";
    if (Serial.available()) {
        delay(10);
        while (Serial.available() > 0) {
            msg += (char)Serial.read();
        }
        Serial.flush();
    }
}

void sendData() {
    Serial.println("data...");
}

void sendAck() {
    Serial.print("gaz: ");
    Serial.print(gaz, DEC);
    Serial.print(", posX: ");
    Serial.print(posX, DEC);
    Serial.print(", posY: ");
    Serial.print(posY, DEC);
    Serial.print(", rotation: ");
    Serial.println(rotation, DEC);
}
