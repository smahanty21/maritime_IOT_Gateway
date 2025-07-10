# main.py

import asyncio
import threading
import time
from modbus_client import ModbusClient
from nmea_client import NMEAClient
from mqtt_publisher import MqttPublisher


def modbus_loop(modbus, publisher):
    modbus.connect()
    print("Modbus polling loop started.")
    while True:
        temps = modbus.read_temperatures()
        if temps:
            for i, temp in temps.items():
                topic = f"ows-challenge/mv-sinking-boat/main-crane/luffing/temp-mot-{i}"
                publisher.publish(topic, f"{temp}°C", "Valid")
        time.sleep(2)  # 0.5 Hz


async def rot_loop(nmea, publisher):
    while True:
        if nmea.current_rot is not None:
            topic = "ows-challenge/mv-sinking-boat/main-crane/rot"
            publisher.publish(topic, f"{nmea.current_rot}°/min", nmea.status)
        await asyncio.sleep(2)  # same frequency


def main():
    modbus = ModbusClient()
    nmea = NMEAClient()
    publisher = MqttPublisher()
    publisher.connect()

    # Start Modbus polling loop in separate thread
    t1 = threading.Thread(target=modbus_loop, args=(modbus, publisher))
    t1.start()

    # Start ROT listener + ROT publish loop
    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(nmea.listen()),
        asyncio.ensure_future(rot_loop(nmea, publisher))
    ]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    main()
