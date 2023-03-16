import os
import math
import random
import paho.mqtt.client as mqtt
import time

id = os.environ.get('BOXID')
# MQTT连接参数
MQTT_BROKER = os.environ.get('NODEIP')
MQTT_PORT = 1883


# msg = {
#     "id": 0,
#     "ip": 0,
#     "timestamp": 0,
#     "data": {
#         "x": 0,
#         "y": 0,
#         "z": 0
#     }
# }

# msg["id"]= os.environ.get('BOXID')


# 发布函数
def publish(client, topic, message):
    client.subscribe(topic, message)


def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode()))

# 连接MQTT服务器
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)

# 订阅一个话题
client.subscribe("input/*")

# 开始循环接收消息
client.loop_forever()
