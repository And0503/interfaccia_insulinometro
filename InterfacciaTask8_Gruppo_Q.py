import tkinter as tk
from tkinter import ttk
import matplotlib as mt
import cmath
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as pt
import asyncio
from threading import Thread
import BackendTask8_Gruppo_Q as bt
from BackendTask8_Gruppo_Q import BluetoothClass as bc

class interface(tk.Tk):
        
    def __init__(self):
    
        super().__init__()
        # Size iniziale
        self.geometry("1080x900")

        # Titolo finestra
        self.title("Insulinometer")
        
        #Bool che blocca creazioni ulteriori di thread
        self.started_thread = False

        #array di dati dal backend
        self.data_array = []
        
        #Inizializzazione componenti grafiche
        self.frequency_step_label = None
        self.frequency_step_text = None
        self.progressbar_label = None
        self.progressbar_frame = None
        self.alerts_text = None
        self.ax1 = None
        self.Module_graph = None
        self.ax2 = None
        self.Phase_graph = None
        self.ax3 = None
        self.Nyquist_graph = None
        self.data_text = None
        self.single_sweep_combobox = None
        self.blt_serial_combobox = None
        self.list = None
        
        
        
        self.turning = 0
        
        
        
        self.backend = bt.BluetoothClass()
        
        #Funzione che crea l'interfaccia
        self.widgets()
        
    def widgets(self):
        
        self.grid_propagate(False)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1, minsize=190)
        self.columnconfigure(5, weight=1, minsize=190)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1, minsize=100)
        self.rowconfigure(3, weight=1, minsize=100)
        self.rowconfigure(4, weight=0)
        
        #GRAFICI
        
        bode_frame1 = tk.LabelFrame(self, text="Module Bode Diagram", height=80, width=100, bg="light blue")
        bode_frame1.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky="nesw")
        bode_frame1.rowconfigure(0, weight=1)
        bode_frame1.columnconfigure(0, weight=1) 
        
        fig, self.ax1 = pt.subplots(layout="constrained", figsize=(5, 3))
        self.ax1.set_ylabel("Magnitude (Db)")
        self.ax1.set_xlabel("Frequency (Hz)")
        self.ax1.set_xscale("log")
        
        self.Module_graph = FigureCanvasTkAgg(fig, master=bode_frame1)
        self.Module_graph.get_tk_widget().grid(row=0, column=0,padx=5, pady=5, sticky="ew", )
        self.Module_graph.draw()
        
        bode_frame2 = tk.LabelFrame(self, text= "Phase Bode Diagram", height=80, width=100, bg="light blue")
        bode_frame2.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky="nesw")
        bode_frame2.rowconfigure(0, weight=1)
        bode_frame2.columnconfigure(0, weight=1)
        
        fig2, self.ax2 = pt.subplots(layout="constrained", figsize=(5, 3))
        self.ax2.set_ylabel("Phase (Deg)")
        self.ax2.set_xlabel("Frequency (Hz)")
        self.ax2.set_xscale("log")
        
        self.Phase_graph = FigureCanvasTkAgg(fig2, master=bode_frame2)
        self.Phase_graph.get_tk_widget().grid(row=0, column=0,padx=5, pady=5, sticky="ew")
        self.Phase_graph.draw()
        
        nyquist_frame = tk.LabelFrame(self, text="Nyquist Diagram", height=80, width=100, bg="light blue")
        nyquist_frame.grid(column=2, row=0, columnspan=2,rowspan=2, padx=5, pady=5, sticky="nesw")
        nyquist_frame.rowconfigure(0, weight=1)
        nyquist_frame.columnconfigure(0, weight=1)

        fig3, self.ax3 = pt.subplots(layout="constrained", figsize=(5, 3))
        self.ax3.set_ylabel("Imaginary Axis")
        self.ax3.set_xlabel("Real Axis")
        
        self.Nyquist_graph = FigureCanvasTkAgg(fig3, master=nyquist_frame)
        self.Nyquist_graph.get_tk_widget().grid(row=0, column=0,padx=5, pady=5, sticky="nsew")
        self.Nyquist_graph.draw()
    
        #OUTPUT FRAMES
        
        #Data
        data_frame = tk.Frame(self, bg="white")
        data_frame.grid(column=4, row=0, columnspan=2, rowspan=2, padx=5, pady=5, sticky="nesw")
        data_frame.rowconfigure(0, weight=0)
        data_frame.rowconfigure(1, weight=1)
        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=0)
        
        data_frame.grid_propagate(True)
        
        data_label = tk.Label(data_frame, text="Data", height=5, width=22, bg="white")
        data_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        
        self.data_text = ttk.Treeview(data_frame, columns=("Frequency (Hz)","Impedance (Ohm)"), show="headings")
        self.data_text.heading("Frequency (Hz)", text="Frequency (Hz)")
        self.data_text.heading("Impedance (Ohm)", text="Impedance (Ohm)")
        
        self.data_text.grid(row=1, column=0, padx=5, pady=5, sticky="news")
        
        #Alerts
        alerts_frame = tk.Frame(self, height=100, width=100, bg="White")
        alerts_frame.grid(column=2, row=2, columnspan=2, rowspan=2, padx=5, pady=5, sticky="nesw")
        alerts_frame.rowconfigure(0, weight=0)
        alerts_frame.rowconfigure(1, weight=0)
        alerts_frame.columnconfigure(0, weight=1)
        alerts_frame.columnconfigure(1, weight=0)
        
        alerts_label = tk.Label(alerts_frame, text="Alerts", height=2, width=22,  bg="white")
        alerts_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        
        self.alerts_text = tk.Text(alerts_frame, height=20, width=65, bg="white", wrap='word')
        self.alerts_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.alerts_text.config(state="normal")
        self.alerts_text.insert(tk.END, "Instructions for use: \n1)Select the Connection Mode\n(if Bluetooth, select the Device) \n2)Select the Frequency Mode \n3)Insert the values \n4)Press Start to begin the measurement \n5)Wait for the data from the server \n\n")
        self.alerts_text.config(state="disabled")
        
        #INPUT FRAMES
        
        #Frequency
        frequency_frame = tk.Frame(self,height=10, width=22, bg="white")
        frequency_frame.grid(column=0, row=2, padx=5, pady=5, sticky="ns")
        frequency_frame.rowconfigure(0, weight=0)
        frequency_frame.rowconfigure(1, weight=0)
        frequency_frame.columnconfigure(0, weight=1)
        
        frequency_label = tk.Label(frequency_frame, text="Frequency" ,height=3, width=30, bg="white")
        frequency_label.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        
        self.frequency_var  = tk.StringVar()
        frequency_text = tk.Entry(frequency_frame, textvariable=self.frequency_var, width=33, bg="white")
        frequency_text.grid(row=1, padx=5, pady=5, sticky="ns")
        
        #Amplitude
        amplitude_frame = tk.Frame(self, height=100, width=200, bg="white")
        amplitude_frame.grid(column=0, row=3, padx=5, pady=5, sticky="n")
        
        amplitude_frame.rowconfigure(0, weight=0)
        amplitude_frame.rowconfigure(1, weight=0)
        amplitude_frame.columnconfigure(0, weight=1)
        
        amplitude_label = tk.Label(amplitude_frame, text="Amplitude" ,height=3, width=30, bg="white")
        amplitude_label.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        
        self.amplitude_var = tk.IntVar()
        amplitude_text = tk.Entry(amplitude_frame, textvariable=self.amplitude_var, width=33, bg="white")
        amplitude_text.grid(row=1, padx=5, pady=5, sticky="ns")
        
        #Single/Sweep ComboBox
        single_sweep_frame = tk.Frame(self, height=100, width=200, bg="white")
        single_sweep_frame.grid(column=1, row=2, padx=5, pady=5, sticky="n")
        single_sweep_frame.rowconfigure(0, weight=0)
        single_sweep_frame.rowconfigure(1, weight=1)
        single_sweep_frame.rowconfigure(2, weight=1)
        
        single_sweep_frame.columnconfigure(0, weight=1)
        
        self.single_sweep_combobox = ttk.Combobox(single_sweep_frame, width=20, state="readonly")
        self.single_sweep_combobox.set("Frequency Mode")
        self.single_sweep_combobox['values']=['Single', 'Sweep']
        self.single_sweep_combobox.grid(row=0, padx=5, pady=5, sticky="ns")
        
        #Chiama la funzione update_single_sweep_combobox alla selezione della modalità di misurazione
        self.single_sweep_combobox.bind("<<ComboboxSelected>>", self.update_single_sweep_combobox)
        
        self.frequency_step_label = tk.Label(single_sweep_frame, text="Frequency Step" ,height=1, width=20, bg="white")
        self.frequency_step_label.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            
        self.frequency_step_var = tk.IntVar()
        self.frequency_step_text = tk.Entry(single_sweep_frame, textvariable=self.frequency_step_var, width=20, bg="white")
        self.frequency_step_text.grid(row=2, padx=5, pady=5, sticky="n")
            
        self.frequency_step_label.grid_forget()
        self.frequency_step_text.grid_forget()
        
        #ProgressBar
        self.progressbar_frame = tk.Frame(self, height=100, width=200, bg="white")
        self.progressbar_frame.grid(column=1, row=3, padx=5, pady=5, sticky="ns")
        self.progressbar_frame.rowconfigure(0, weight=0)
        self.progressbar_frame.rowconfigure(1, weight=0)
        self.progressbar_frame.rowconfigure(2, weight=0)
        self.progressbar_frame.rowconfigure(3, weight=1)   
        self.progressbar_frame.columnconfigure(0, weight=1)

        self.progressbar_label = tk.Label(self.progressbar_frame, text="Progress Bar" ,height=1, width=22, bg="white")
        self.progressbar_label.grid(row=2, column=0, padx=5, pady=5, sticky="s")
            
        progressbar = ttk.Progressbar(self.progressbar_frame, length=100)
        progressbar.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            
        self.progressbar_frame.grid_forget()
        self.progressbar_label.grid_forget()
        
        #Cycles
        cycles_label = tk.Label(self.progressbar_frame, text="Cycles" ,height=1, width=22, bg="white")
        cycles_label.grid(row=0, column=0, padx=5, pady=5, sticky="s")
        
        self.cycles_var = tk.IntVar()
        cycles_text = tk.Entry(self.progressbar_frame, textvariable=self.cycles_var, width=20, bg="white")
        cycles_text.grid(row=1, padx=5, pady=5, sticky="ns")
        
        #Battery        
        battery_frame = tk.Frame(self, height=100, width=350, bg="green")
        battery_frame.grid(column=4, row=3, columnspan=2, padx=5, pady=5, sticky="ns")
        battery_frame.rowconfigure(0, weight=0)
        battery_frame.rowconfigure(1, weight=0)
        battery_frame.columnconfigure(0, weight=0)
        battery_frame.columnconfigure(1, weight=0)
        
        battery_label = tk.Label(battery_frame, text="Battery", height=5, width=22, bg="white")
        battery_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ns")

        #Bluetooth/Serial ComboBox
        blt_serial_frame = tk.Frame(self, height=100, width=200, bg="white")
        blt_serial_frame.grid(column=4, row=2, columnspan=2, padx=5, pady=5, sticky="n")
        blt_serial_frame.rowconfigure(0, weight=0)
        blt_serial_frame.rowconfigure(1, weight=0)
        
        self.blt_serial_combobox = ttk.Combobox(blt_serial_frame, width=20, state="readonly")
        self.blt_serial_combobox.set("Connection Mode")
        self.blt_serial_combobox['values']=['Bluetooth', 'Serial']
        self.blt_serial_combobox.grid(row=0, columnspan=2, padx=5, pady=5, sticky="n")
        
        self.list = tk.Listbox(blt_serial_frame, height=5, width=50)
        self.list.grid(row=1, padx=5, pady=5, sticky="n")
        
        self.list.grid_forget()
        
        self.blt_serial_combobox.bind("<<ComboboxSelected>>", self.update_blt_serial)
        self.list.bind("<<ListboxSelect>>", lambda event, listbox=self.list, devices=self.backend.device_list:self.on_device_select(event, listbox, devices))
        
        #BUTTONS
        
        start_button = tk.Button(self, text="Start", height=3, width=22, bg="light blue", command= self.start_button_click)
        start_button.grid(column=0, row=4, padx=5, pady=5, sticky="ns")
        
        addmarker_button = tk.Button(self, text="Add Marker", height=3, width=22, bg="light blue", command= self.addmarker_button_click)
        addmarker_button.grid(column=1, row=4, padx=5, pady=5, sticky="ns")
        
        resetbuffer_button = tk.Button(self, text="Reset Buffer", height=3, width=22, bg="light blue", command= self.resetbuffer_button_click)
        resetbuffer_button.grid(column=2, row=4, padx=5, pady=5, sticky="ns")
        
        export_button = tk.Button(self, text="Export", height=3, width=22, bg="light blue", command= self.export_button_click)
        export_button.grid(column=3, row=4, padx=5, pady=5, sticky="ns")
        
        clear_button = tk.Button(self, text="Clear", height=3, width=22, bg="light blue", command= self.clear_button_click)
        clear_button.grid(column=4, row=4, padx=5, pady=5, sticky="ns")
        
        differential_button = tk.Button(self, text="Differential", height=3, width=22, bg="light blue", command= self.differential_button_click)
        differential_button.grid(column=5, row=4, padx=5, pady=5, sticky="ns")
    
    #FUNCTIONS
        
    #Funzione eseguita da un thread separato che chiama la funzione async Scanner() dal backend
    def run_scanner(self):
        device_list = asyncio.run(self.backend.Scanner())
        self.list.delete(0, tk.END)
        for device in device_list:
            self.list.insert(tk.END, device)
    
    #Selezione modalità di connessione + thread per lo scanner
    def update_blt_serial(self, event):
        selected_value = self.blt_serial_combobox.get()
    
        if selected_value == 'Bluetooth':
            self.list.grid(row=1, padx=5, pady=5, sticky="n")
            Thread(target=self.run_scanner).start() #Variabile booleana da aggiungere
             
        if selected_value == 'Serial':
            self.list.grid_forget()
        
    #Funzione di selezione del dispositivo a cui collegarsi
    def on_device_select(self, event, listbox, devices):
        selected_index = listbox.curselection()# Ottieni l'indice dell'elemento selezionato
        if selected_index:
            selected_device = devices[selected_index[0]] # Ottieni il dispositivo dalla lista
            device_address = selected_device.split(": ")[1]
            print(f"Connecting to device: {selected_device.split(": ")[0]} - {device_address}")
            Thread(target=self.selected_connection, args=(device_address,)).start()
    
    def selected_connection(self, device_address):
        client = self.backend.connect_in_thread(device_address)
        if client == None:
            self.alerts_text.config(state='normal')
            self.alerts_text.insert(tk.END, f"Connection failed \n\n")
            self.alerts_text.config(state='disabled')
        else:
            if client.is_connected:
                self.alerts_text.config(state='normal')
                self.alerts_text.insert(tk.END, f"Connected to device: {device_address} \n\n")
                self.alerts_text.config(state='disabled')  
        
    #Funzione che aggiorna l'interfaccia del single_sweep_combobox
    def update_single_sweep_combobox(self, event):
            selected_value = self.single_sweep_combobox.get()
            
            if selected_value == 'Sweep':
                self.frequency_step_label.grid(row=1, column=0, padx=5, pady=5, sticky="n")
                self.frequency_step_text.grid(row=2, padx=5, pady=5, sticky="n")
                self.progressbar_frame.grid(column=1, row=3, padx=5, pady=5, sticky="ns")
                self.progressbar_label.grid(row=2, column=0, padx=5, pady=5, sticky="s")
                
                self.alerts_text.config(state="normal")
                self.alerts_text.insert(tk.END, "Selected Sweep Mode: \n")
                self.alerts_text.insert(tk.END, "Insert the initial frequency and the final frequency in the Frequency field separated by - \n\n")                
                self.alerts_text.config(state="disabled")
                
                #prende data sweep inviato dal server al backend
                self.backend.frontend_update_function = self.collect_data_sweep

            if selected_value == 'Single':
                self.frequency_step_label.grid_forget()
                self.frequency_step_text.grid_forget()
                self.progressbar_frame.grid_forget()
                self.progressbar_label.grid_forget()
                
                self.alerts_text.config(state="normal")
                self.alerts_text.insert(tk.END, "Selected Single Mode \n\n")
                self.alerts_text.config(state="disabled")
                
                #prende data single inviato dal server al backend
                self.backend.frontend_update_function = self.update_data_single  
        
    def update_data_single(self, sender, data):        
        
        # Decodifica e aggiorna la data table
        data = data.decode('UTF-8')
        z = complex(data)
        
        self.data_text.insert('', 'end', values=(int(self.frequency_var.get()), z))
        print(f"Dati ricevuti dal server: {data}")
        print(f"Sender: {sender}")    
        
        #Grafico del modulo
        self.ax1.plot(int(self.frequency_var.get()), abs(z), marker="o")
        self.Module_graph.draw()
        
        #Grafico della fase
        self.ax2.plot(int(self.frequency_var.get()), cmath.phase(z), marker="o")
        self.Phase_graph.draw()
        
        #Nyquist
        self.ax3.plot(z.real, z.imag, marker="o")
        self.Nyquist_graph.draw()
       
    def update_data_sweep(self):
        frequency = self.frequency_var.get()
        step = self.frequency_step_var.get()
        initial_frequency_value = int(frequency.split('-')[0])
                
        i = 0
        graph_frequency_list = []
        module_list = []
        phase_list = []
        real_list = []
        imaginary_list = []
        
        for z in self.data_array:
        
            graph_frequency = initial_frequency_value + i * step
            graph_frequency_list.append(graph_frequency)
            module_list.append(abs(z))
            phase_list.append(cmath.phase(z))
            real_list.append(z.real)
            imaginary_list.append(z.imag)
            self.data_text.insert('', 'end', values=(graph_frequency, z))
            
            i = i+1
            
        #Grafico del modulo
        self.ax1.plot(graph_frequency_list, module_list, marker="o", linestyle = "-")
        self.Module_graph.draw()
            
        #Grafico della fase
        self.ax2.plot(graph_frequency_list, phase_list, marker="o", linestyle = "-")
        self.Phase_graph.draw()
            
        #Nyquist
        self.ax3.plot(real_list, imaginary_list, marker="o", linestyle = "-")
        self.Nyquist_graph.draw()
            
    def collect_data_sweep(self, sender, data):
        
        data = data.decode('UTF-8')
        self.data_array.append(complex(data))
        
        frequency = self.frequency_var.get()
        
        initial_frequency_value = int(frequency.split('-')[0])
        final_frequency_value = int(frequency.split('-')[1])
        frequency_step = self.frequency_step_var.get()
        #cycle = self.cycles_var.get()
        
        if len(self.data_array) == ((final_frequency_value - initial_frequency_value) / frequency_step) + 1 :
            
            self.update_data_sweep()
            self.data_array.clear()
        
    def sending_thread(self):  
        #Crea un thread per inviare valori senza bloccare l'interfaccia.
        # try:
        #     frequency = self.frequency_var.get()
    
        #     if '-' in frequency: 
        #         initial_frequency_value = int(frequency.split('-')[0])
        #         final_frequency_value = int(frequency.split('-')[1])
        #     else:
        #         final_frequency_value = int(0) 
        #         initial_frequency_value = int(frequency)
            
        #     amplitude_value = self.amplitude_var.get()
        #     frequency_step = self.frequency_step_var.get()
        #     cycles_value = self.cycles_var.get()

        #     values = [amplitude_value, initial_frequency_value, final_frequency_value, frequency_step, cycles_value]
        #     thread = Thread(target=self.run_send_value, args=(values,))
        #     thread.start()
        try:
            
            self.turning = self.turning + 1
            value = self.turning % 2
            if (value == 0 or value == 1):
                thread = Thread(target=self.run_send_value, args=(value,))
                thread.start()
            
        except ValueError:
            print("Valore non valido. Inserisci un numero intero.")
            return None
        
    def run_send_value(self, value):
        #Invia i valori usando la funzione asincrona `send_value`
            # asyncio.run(self.backend.send_value(values[0], bc.AMPLITUDE_UUID))
            # asyncio.run(self.backend.send_value(values[1], bc.INITIAL_FREQUENCY_UUID))
            # asyncio.run(self.backend.send_value(values[2], bc.FINAL_FREQUENCY_UUID))
            # asyncio.run(self.backend.send_value(values[3], bc.FREQUENCY_STEP_UUID))
            # asyncio.run(self.backend.send_value(values[4], bc.CYCLE_UUID))
        asyncio.run(self.backend.send_value(value, bc.ESP32_UUID))
            
            
    
    def impedance(self):
        asyncio.run(self.backend.listen_for_data())
    
    def impedance_thread(self):
        if not self.started_thread:
            self.started_thread = True
            thread = Thread(target=self.impedance)
            thread.start() 

    #Buttons Functions
    def start_button_click(self):
        
        self.sending_thread()
        #self.impedance_thread()
        
    def addmarker_button_click(self):
        print("Add Marker")
        
    def resetbuffer_button_click(self):
        print("Reset Buffer")
        
    def export_button_click(self):
        print("Export")
        
    def clear_button_click(self):
        self.data_text.delete(*self.data_text.get_children())
        self.ax1.cla()
        self.ax1.set_ylabel("Magnitude (Db)")
        self.ax1.set_xlabel("Frequency (Hz)")
        self.ax1.set_xscale("log")
        self.Module_graph.draw()
        
        self.ax2.cla()
        self.ax2.set_ylabel("Phase (Deg)")
        self.ax2.set_xlabel("Frequency (Hz)")
        self.ax2.set_xscale("log")
        self.Phase_graph.draw()
        
        self.ax3.cla()
        self.ax3.set_ylabel("Imaginary Axis")
        self.ax3.set_xlabel("Real Axis")
        self.Nyquist_graph.draw()
        
        print("Cleared data and graphs")
        
    def differential_button_click(self):
        print("Differential")
        
if __name__ == "__main__":
    app = interface()
    app.configure(bg="white")
    app.mainloop()