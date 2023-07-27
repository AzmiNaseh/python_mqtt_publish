import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.tls_set(ca_certs="./caMqttRoot.crt", certfile="mqttBroker.crt", keyfile="mqttBroker.key")
client.username_pw_set("username", "password")
client.on_connect = on_connect
client.connect("something.domain.com", 8883, 60)

client.publish("python/test", "one time publish from my local system")

client.disconnect()

