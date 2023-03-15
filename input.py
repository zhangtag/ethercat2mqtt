import math
import random
import paho.mqtt.client as mqtt
import time

# MQTT连接参数
MQTT_BROKER = "192.168.1.233"
MQTT_PORT = 1883
boxid=0
nodeip=0
xa=0
ya=0
za=0
msg = {
    "id": boxid,
    "ip": nodeip,
    "timestamp": int(time.time() * 1000),
    "data": {
        "x": xa,
        "y": ya,
        "z": za
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
    for i in range(20):
        xa = math.sin(2 * math.pi * x / 68) + random.uniform(-0.001, 0.001)
        
        # 将y发布到MQTT服务器
        MQTT_TOPIC = "input/box{i}"
        boxid = i
        publish(client, MQTT_TOPIC, str(msg))
        
        # 休眠20毫秒
        time.sleep(0.02)
