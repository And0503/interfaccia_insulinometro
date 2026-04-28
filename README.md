# interfaccia_insulinometro

## Descrizione del progetto
- Interfaccia per un insulinometro sperimentale che integra un sistema di analisi di bioimpedenza per il monitoraggio del sito di iniezione. 
- Il dispositivo applica una piccola tensione alternata a bassa intensità tramite elettrodi posizionati nell’area di interesse. Misurando la corrente risultante è possibile stimare l’impedenza elettrica del tessuto.
- L’impedenza può variare in funzione della composizione e struttura del tessuto sottocutaneo. Variazioni locali di impedenza possono essere associate a differenze nella distribuzione del tessuto adiposo o alla presenza di tessuto fibrotico/cicatriziale, condizioni che possono influenzare la regolarità dell’assorbimento dell’insulina.


- Supporta la modalità:
  - Single: per misurazione a frequenza singola (consente una misurazione rapida)
  - Sweep: per misurazione a frequenza variabile, da start a stop con step incrementale (permette la caratterizzazione completa del comportamento in frequenza del tessuto)
 

Include:
1. Interfaccia grafica adattiva realizzata con **Tkinter**
2. Comunicazione tramite **Bluetooth Low Energy (BLE)**
3. Visualizzazione dell’impedenza tramite diagrammi di Bode e Nyquist con **Matplotlib**

---

---
## 👥 Autori
- Andrea Tito - https://github.com/And0503 
- Flavio Soldatini - https://github.com/FlavioSol
---

---
## Interfaccia grafica

<img width="1716" height="913" alt="image" src="https://github.com/user-attachments/assets/e7d5a3ae-28cc-45e9-863a-d71d298b8edf" />

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
# 🚀 Come eseguire il progetto

Scaricare i file Python di interfaccia e backend.

Per avviare il programma basta eseguire il file di interfaccia.

---

## 📡 GATT Server

1. Scaricare **nRF Connect for Mobile**
2. Importare il file `insulinometer.xml` nella sezione **Configure GATT Server**
3. I valori inviati dal programma verranno visualizzati all’interno dei registri
4. Per inviare i valori:
   - accedere al registro **Impedance**
   - inserire i dati in formato **TEXT UTF-8**
   - per numeri complessi usare il formato `a+bj`
   - selezionare **Notification** in Advanced
   - premere **Send**
---

## ⚙️ ESP32

1. Caricare il file `.ino` sulla board
2. Avviare il file `InterfacciaESP.py`
3. Selezionare Bluetooth e collegarsi alla board
4. Ad ogni pressione del tasto **Start**, il LED si accende/spegne

---

---
## ⚠️ Nota che...

L’interfaccia è un prototipo e non è completa in tutte le sue funzionalità.

In particolare, i seguenti elementi non sono ancora implementati:

- Funzionalità associate ai pulsanti:
  - Add Marker
  - Reset Buffer
  - Export
  - Differential

- Funzionalità di sistema:
  - Controllo del livello della batteria dell’insulinometro
  - Connessione seriale

Inoltre, il sistema non è stato ancora validato sperimentalmente con un insulinometro reale.

---
