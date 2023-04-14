import pysoem
# import sys
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


class El1259ConfigFunction:

    def __init__(self, device):
        self._device = device

    def fn(self, slave_pos):
        """
        struct format characters
        B - uint8
        x - pac byte
        H - uint16
        """

        self._device.sdo_write(0x8001, 2, struct.pack('B', 1))

        rx_map_obj = [0x1603, 0x1607, 0x160B, 0x160F, 0x1613, 0x1617, 0x161B, 0x161F,
                      0x1620, 0x1621, 0x1622, 0x1623, 0x1624, 0x1625, 0x1626, 0x1627]
        pack_fmt = 'Bx' + ''.join(['H' for _ in range(len(rx_map_obj))])
        rx_map_obj_bytes = struct.pack(pack_fmt, len(rx_map_obj), *rx_map_obj)
        self._device.sdo_write(0x1c12, 0, rx_map_obj_bytes, True)

        tx_map_obj = [0x1A00, 0x1A01, 0x1A02, 0x1A03, 0x1A04, 0x1A05, 0x1A06, 0x1A07, 0x1A08,
                      0x1A0C, 0x1A10, 0x1A14, 0x1A18, 0x1A1C, 0x1A20, 0x1A24]
        pack_fmt = 'Bx' + ''.join(['H' for _ in range(len(tx_map_obj))])
        tx_map_obj_bytes = struct.pack(pack_fmt, len(tx_map_obj), *tx_map_obj)
        self._device.sdo_write(0x1c13, 0, tx_map_obj_bytes, True)

        self._device.dc_sync(1, 1000000)


# @pytest.mark.parametrize('overlapping_enable', [False, True])
def test_io_toggle(pysoem_env, overlapping_enable):
    pysoem_env.config_init()
    el1259 = pysoem_env.get_el1259()
    pysoem_env.el1259_config_func = El1259ConfigFunction(el1259).fn
    pysoem_env.config_map(overlapping_enable)
    pysoem_env.go_to_op_state()

    output_len = len(el1259.output)

    tmp = bytearray([0 for _ in range(output_len)])

    for i in range(8):
        out_offset = 12 * i
        in_offset = 4 * i

        tmp[out_offset] = 0x02
        el1259.output = bytes(tmp)
        time.sleep(0.1)
        assert el1259.input[in_offset] & 0x04 == 0x04

        tmp[out_offset] = 0x00
        el1259.output = bytes(tmp)
        time.sleep(0.1)
        assert el1259.input[in_offset] & 0x04 == 0x00
        
def main(ifname):
    # Create EtherCAT master
    master = pysoem.Master()
    master.open(ifname)

    if master.config_init() > 0:
        # Map slave configurations
        master.config_map()

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
                

                # for idx, slave in enumerate(master.slaves, start=1):
                #     # print(f"Slave {idx} (ID: {slave.configadr}):")
                #     # for i, data in enumerate(slave.inputs):
                #     #     print(f"  Input {i}: {data}")
                #     # for i, data in enumerate(slave.outputs):
                #     #     print(f"  Output {i}: {data}")
                #     # print()
                # Iterate over all slaves and publish their data to MQTT
                for idx, slave in enumerate(master.slaves, start=1):
                    message = slave.receiveddatagram
                    topic = f"ethercat/box{idx}"
                    client.publish(topic, message)
                # Add a delay to avoid flooding the console
                time.sleep(1)

        except KeyboardInterrupt:
            print("Stopping...")

        # Set all slaves to pre-operational state
        master.state = pysoem.PREOP_STATE
        master.write_state()

    else:
        print("No slaves found")

    # Close EtherCAT master
    master.close()
    client.disconnect()

if __name__ == "__main__":
    main("enp1s0")
