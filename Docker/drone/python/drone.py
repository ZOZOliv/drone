import paho.mqtt.client as mqtt
import time

# Callback exécutée lors de la connexion
def on_connect(client, userdata, flags, rc) :
    print("Connected with result code "+str(rc))
    # Après la connexion, nous nous abonnons aux topics
    client.subscribe("drone/#")

# Callback exécutée lors de la déconnexion
def on_disconnect(client, userdata, rc) :
    print("Déconnecté")

# Callback exécutée lors d'un nouveau message
def on_message(client, userdata, msg) :
    # Nous imprimons chaque message reçu
    info = '{topic} : {value}'.format(topic = msg.topic, value = msg.payload.decode("utf-8"))
    print(info)

# Lancement du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set("user", "user") # user/password
#client.tls_set()
client.connect("10.205.224.68", 1883, 60)
client.loop_start()

try:
    while True:
        client.publish("drone/altitude", "22")
        client.publish("drone/angle", "x:10;y:20;z:30")
        time.sleep(10)

except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect_callback()
    client.disconnect()