import paho.mqtt.client as mqtt
import time
# MQTT 服务器信息
mqtt_broker = "192.168.1.233"
mqtt_port = 1883
mqtt_username = "1"
mqtt_password = "1"

# 连接到MQTT服务器
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.connect(mqtt_broker, mqtt_port, 60)

# 发布消息
while True:
    topic = "test"
    message = "vscode"
    client.publish(topic, message)
    time.sleep(1)
# 断开连接

client.disconnect()
