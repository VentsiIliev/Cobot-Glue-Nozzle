from GlueDispensingApplication.modbusCommunication.ModbusClient import ModbusClient


class ModbusClientSingleton:
    _client_instance = None  # Static variable to hold the instance

    @staticmethod
    def get_instance(slave=10, port='COM5', baudrate=115200, bytesize=8, stopbits=1, timeout=0.01):
        if ModbusClientSingleton._client_instance is None:
            ModbusClientSingleton._client_instance = ModbusClient(slave, port, baudrate, bytesize, stopbits, timeout)
        return ModbusClientSingleton._client_instance



