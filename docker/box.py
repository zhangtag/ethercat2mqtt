import os
import json
import paho.mqtt.client as mqtt
# import time

# id = os.environ.get('BOXID')
# MQTT连接参数
MQTT_BROKER = os.environ.get('NODEIP')  
MQTT_PORT = 1883
# MQTT_BROKER = "192.168.1.110"
MQTT_TOPIC = "out/box%d" % int(os.environ.get('BOXID')) 
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


# 定义回调函数来处理收到的消息
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    msg["id"] = os.environ.get('BOXID')
    msg["data"]["x"] = data["data"]["x"]
    client.publish(MQTT_TOPIC, json.dumps(msg))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("input/#")

# 连接MQTT服务器
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT)  # 连接到MQTT broker
except ConnectionRefusedError:
    print("连接被拒绝,请确认broker地址是否正确或服务已启动")
    exit()

# 开始循环接收消息
client.loop_forever()
