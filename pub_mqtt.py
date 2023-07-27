import paho.mqtt.client as mqtt
import time
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
from google.cloud.firestore_v1 import DocumentSnapshot


cred = credentials.Certificate("/home/ubuntu/myproject/something-firebase-adminsdk-c4567v-wdrgr4453g.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection('something').order_by('Timestamp', direction=firestore.Query.ASCENDING).stream()


# Find the last modified document from firebase database
last_modified_doc = None
for doc in docs:
    if isinstance(doc, DocumentSnapshot):
        if last_modified_doc is None:
            last_modified_doc = doc
        else:
            if last_modified_doc.update_time < doc.update_time:
                last_modified_doc = doc

# Print the last modified document
last_mod_doc = {}
if last_modified_doc is not None:
    last_mod_doc[last_modified_doc.id]= last_modified_doc.to_dict()
    print (last_mod_doc)
else:
    print('No documents found')



Connected = ""
def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection 

    else:

        print("Connection failed")


broker_address= "something.domain.com"
port = 8883
user = "username"
password = "password"

#client = mqttClient.Client("Python")
client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.username_pw_set(user, password=password)
client.on_connect= on_connect
client.connect(broker_address, port=port)

client.tls_set("./caMqttRoot.crt")      #path to your .crt file

client.loop_start()

while Connected != True:                #Wait for connection
    time.sleep(0.1)


try:
#    while True:
        client.publish("python/test",f'{last_mod_doc}')
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
