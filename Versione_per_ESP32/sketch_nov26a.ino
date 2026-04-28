#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

// UUID per il servizio e la caratteristica
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

// Pin del LED
const int ledPin = 2;  // Modifica con il pin del LED

volatile int on_off = 0;

// Classe di callback per la ricezione dei dati
class MyCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();

    if (value.length() > 0) {
      Serial.print("Valore ricevuto: ");
      for (int i = 0; i < value.length(); i++) {
        Serial.print(value[i]);
      }
      Serial.println();

      // Convertire il valore in intero
      on_off = atoi(value.c_str());
    }
  }
};

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  Serial.println("Inizializzazione BLE...");

  // Creazione del dispositivo BLE
  BLEDevice::init("ESP32-BLE");

  // Creazione del server BLE
  BLEServer *pServer = BLEDevice::createServer();

  // Creazione del servizio BLE
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Creazione della caratteristica BLE
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                          CHARACTERISTIC_UUID,
                                          BLECharacteristic::PROPERTY_READ |
                                          BLECharacteristic::PROPERTY_WRITE
                                        );

  // Impostare il callback per la scrittura dei dati
  pCharacteristic->setCallbacks(new MyCallbacks());

  // Avvio del servizio
  pService->start();

  // Avvio della pubblicità BLE
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->start();

  Serial.println("BLE pronto. In attesa di connessioni...");
}

void loop() {
  // Lampeggia il LED con l'intervallo specificato
  if (on_off == 1){

    digitalWrite(ledPin, HIGH);

  }else if (on_off == 0) {

    digitalWrite(ledPin, LOW);

  }
  delay(1000); 
}
