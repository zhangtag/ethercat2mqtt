import pysoem
import sys
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

topic = "ethercat"

def main(ifname):
    # Create EtherCAT master
    master = pysoem.Master()
    master.open(ifname)

    if master.config_init() > 0:
        # Map slave configurations
        master.config_map()

        # Check for 10 expected slaves
        if len(master.slaves) == 10:
            # Configure Distributed Clocks (DC) if required
            # This is optional and depends on your EtherCAT network configuration
            master.config_dc()

            # Set operational state for all slaves
            master.state_check(pysoem.SAFEOP_STATE, 50000)
            master.state = pysoem.OP_STATE
            master.write_state()

            # Wait for all slaves to reach operational state
            master.state_check(pysoem.OP_STATE, 50000)

            try:
                while True:
                    # Read process data
                    master.send_processdata()
                    master.receive_processdata(5000)

                    for idx, slave in enumerate(master.slaves, start=1):
                        # print(f"Slave {idx} (ID: {slave.configadr}):")
                        # for i, data in enumerate(slave.inputs):
                        #     print(f"  Input {i}: {data}")
                        # for i, data in enumerate(slave.outputs):
                        #     print(f"  Output {i}: {data}")
                        # print()
                        message = slave.sdo_read(0x6050,1,8)

                    # Add a delay to avoid flooding the console
                    time.sleep(1)

            except KeyboardInterrupt:
                print("Stopping...")

            # Set all slaves to pre-operational state
            master.state = pysoem.PREOP_STATE
            master.write_state()
        else:
            print(f"Expected 10 slaves, but found {len(master.slaves)}")
    else:
        print("No slaves found")

    # Close EtherCAT master
    master.close()

if __name__ == "__main__":
    main("enp1s0")
    # if len(sys.argv) > 1:
    #     main(sys.argv[1])
    # else:
    #     print("Usage: python ethercat_data_print.py <network_interface>")