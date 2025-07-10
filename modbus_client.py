# modbus_client.py

from pymodbus.client import ModbusTcpClient


class ModbusClient:
    def __init__(self, host='127.0.0.1', port=8889, unit=1):
        self.client = ModbusTcpClient(host=host, port=port)
        self.unit = unit

    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

    def read_temperatures(self):
        """
        Read 4 holding registers for 4 temperature sensors.
        Returns a dict like {1: temp1, 2: temp2, 3: temp3, 4: temp4}
        """
        try:
            result = self.client.read_holding_registers(0, 4, unit=self.unit)
            if result.isError():
                print(f"Modbus error: {result}")
                return None
            temps = {}
            for i, reg in enumerate(result.registers, 1):
                temps[i] = reg
            return temps
        except Exception as e:
            print(f"Modbus exception: {e}")
            return None
