from bleak import BleakScanner, BleakClient

import asyncio

device_address = ""

AMPLITUDE_UUID = "00001001-0000-1000-8000-00805f9b34fb"
INITIAL_FREQUENCY_UUID = "00001002-0000-1000-8000-00805f9b34fb"
FINAL_FREQUENCY_UUID = "00001003-0000-1000-8000-00805f9b34fb"
FREQUENCY_STEP_UUID = "00001004-0000-1000-8000-00805f9b34fb"
CYCLE_UUID = "00001005-0000-1000-8000-00805f9b34fb"
IMPEDANCE_UUID = "00001006-0000-1000-8000-00805f9b34fb"

client = BleakClient(device_address)

async def Scanner():

    device_list = []
    
    devices = await BleakScanner.discover(timeout=10.0)
    for device in devices:
        device_list.append((device.name or "Unknown", device.address))
    
    return device_list

async def Connect_to_device(device_address):
    
    global client
    
    client = BleakClient(device_address)
    connected = await client.connect()
    if connected:
        print(f"Connected to device: {device_address}")
        return connected #ritorna l'oggetto client in modo da poterci interagire
    else:
        print(f"Failed to connect to device: {device_address}")
     
async def send_value(value, UUID):
    global client
    print(client)
    try:                              
        # Converte il valore in byte e invia il valore al registro
        bytes = value.to_bytes(2, byteorder='little')                
        await client.write_gatt_char(UUID, bytes)                
        print(f"{value} sent to UUID={UUID}")
    except Exception as e:
        print(f"Error sending value: {e}")
        
frontend_update_function = None

def notification_callback(sender: str, data: bytearray):
    if frontend_update_function:
        frontend_update_function(sender, data)
        
# Funzione asincrona per connettersi al dispositivo e iscriversi alle notifiche
async def listen_for_data():
    global client
            
    # Iscrizione alle notifiche della caratteristica
    await client.start_notify(IMPEDANCE_UUID, notification_callback)

    while True:
        await asyncio.sleep(1)        
               
async def Disconnect_from_device():
    global client
    if client and client.is_connected:
        await client.disconnect()
        print("Disconnected from the device.")
