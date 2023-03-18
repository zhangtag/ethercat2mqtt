import os
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = os.environ.get('NODEIP', '192.168.1.233')  
MQTT_PORT = 1883
MQTT_TOPIC = "out/box%d" % int(os.environ.get('BOXID', 0)) 

msg = {
    "id": 0,
    "ip": 0,
    "timestamp": 0,
    "data": {
        "x": 0,
        "y": 0,
        "z": 0
    }
}

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    msg["id"] = os.environ.get('BOXID', 0)
    msg["data"]["x"] = data["data"]["x"]
    client.publish(MQTT_TOPIC, json.dumps(msg))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("input/#")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT)
except ConnectionRefusedError:
    print("连接被拒绝,请确认broker地址是否正确或服务已启动")
    exit()

client.loop_forever()
