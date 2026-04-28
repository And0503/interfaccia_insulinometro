from bleak import BleakScanner, BleakClient
from threading import Thread
import bleak

import asyncio

class BluetoothClass():
    
    AMPLITUDE_UUID = "00001001-0000-1000-8000-00805f9b34fb"
    INITIAL_FREQUENCY_UUID = "00001002-0000-1000-8000-00805f9b34fb"
    FINAL_FREQUENCY_UUID = "00001003-0000-1000-8000-00805f9b34fb"
    FREQUENCY_STEP_UUID = "00001004-0000-1000-8000-00805f9b34fb"
    CYCLE_UUID = "00001005-0000-1000-8000-00805f9b34fb"
    IMPEDANCE_UUID = "00001006-0000-1000-8000-00805f9b34fb"
    ESP32_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    
    def __init__(self):
        self.client = None
        self.device_address = ""
        self.device_list = []
        self.frontend_update_function = None
        
    async def Scanner(self):
        self.device_list.clear() #Lista di stringhe (Nome + address)
        #found_devices è un lista di BLEDevices
        found_devices = await BleakScanner.discover(timeout=10.0)
        for device in found_devices:
            self.device_list.append(str(device.name) + ": " + str(device.address))
        return self.device_list
                
    def connect_in_thread(self, device_address):
        # Chiama la funzione per connettersi al dispositivo
        self.device_address = device_address
        self.client = asyncio.run(self.Connect_to_device())
        return self.client
        
    async def Connect_to_device(self):
        self.client = BleakClient(self.device_address)
        try:
            await self.client.connect()
            print(f"Connected to device: {self.device_address}")
            return self.client
        except bleak.BleakError as e:
            print(e)
        
    async def send_value(self, value, UUID):
        try:                              
            # Converte il valore in byte e invia il valore al registro
            onoff = str(value).encode('UTF-8')                
            await self.client.write_gatt_char(UUID, onoff)                
            print(f"{value} sent to UUID={UUID}")
        except Exception as e:
            print(f"Error sending value: {e}")

    def notification_callback(self, sender: str, data: bytearray):
        print(data.decode('UTF-8'))
        if self.frontend_update_function:
            self.frontend_update_function(sender, data)
            
    # Funzione asincrona per connettersi al dispositivo e iscriversi alle notifiche
    async def listen_for_data(self):
        # Iscrizione alle notifiche della caratteristica
        await self.client.start_notify(self.IMPEDANCE_UUID, self.notification_callback)

        while True:
            await asyncio.sleep(1)        
                
    async def Disconnect_from_device(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print("Disconnected from the device.")