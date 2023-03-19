import math
import random
import paho.mqtt.client as mqtt
import time
import json
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# MQTT连接参数
# MQTT_BROKER = "192.168.1.233"
MQTT_PORT = 1883
MQTT_BROKER = "192.168.1.131"

msg = {
    "boxid": 0,
    # "now": hostname,
    "original":ip_address,
    "timestamp": int(time.time() * 1000),
    "data": {
        "x": 0,
        "y": 0,
        "z": 0
    }
}


# 发布函数
def publish(client, topic, message):
    client.publish(topic, message)

# 连接MQTT服务器
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

x=0
# 循环发布数据
while True:
    # 计算函数值并加上随机数
    x += 1
    if x > 68:
        x = 0
    for i in range(1,21):
        msg["data"]["x"] = math.sin(2 * math.pi * x / 68 + 10) + random.uniform(-0.001, 0.001)
        msg["data"]["y"] = math.sin(2 * math.pi * x / 68 + 20) + random.uniform(-0.001, 0.001)
        msg["data"]["z"] = math.sin(2 * math.pi * x / 68 + 30) + random.uniform(-0.001, 0.001)
        # 将y发布到MQTT服务器
        MQTT_TOPIC = "input/box%d" % i
        msg["boxid"] = i
        publish(client, MQTT_TOPIC, json.dumps(msg))
        
        # 休眠20毫秒
    time.sleep(0.02)
