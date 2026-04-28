# interfaccia_insulinometro

## Descrizione del progetto
Interfaccia per un insulinometro sperimentale che integra un sistema di analisi di bioimpedenza per il monitoraggio del sito di iniezione. 

Include:
1. Interfaccia realizzata con Tkinter
2. Comunicazione tramite Bluetooth Low Energy (BLE)
3. Visualizzazione dell’impedenza tramite diagrammi di Bode e Nyquist con Matplotlib

---
## 👥 Autori
- Andrea Tito - https://github.com/And0503 
- Flavio Soldatini - https://github.com/FlavioSol
---

---
## ⚙️ Guida tecnica
---

---
### 🛠️ Tecnologie
- Visual Studio Code
- Python 3.13.9 
  - Tkinter 8.6 (standard library)
  - matplotlib 3.10.7
  - bleak 3.0.1
- nRF connect for mobile di Nordic Semiconductor ASA versione 4.29.1
- Esp32-wroom-32
---

---

### 📁 Struttura del repo
| File | Descrizione |
|------|-------------|

---

---
### 🚀 Come eseguire il progetto
**GATT Server**
  1. scaricare nRF connect for mobile
  2. Importare il file insulinometer.xml in allegato nella sezione Configure GATT Server
  3. I valori inviati dal programma verranno visualizzati all’interno dei registri
  4. Per inviare i valori accedere al registro Impedance e inserirli col formato TEXT UTF-8 (i numeri complessi vanno inviati nel formato a+bj), selezionando Notification in Advanced

**ESP32**
  1.  Caricare il file .ino nella board
  2.  Avviare il file InterfacciaESP.py
  3.  Selezionare Bluetooth e collegarsi alla board
  4.   Ad ogni pressione del tasto Start il led si accenderà/spegnerà
---
