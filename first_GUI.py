import tkinter as tk
import pandas as pd
class ColdLab:
    def __init__(self,root):
        self.menubar = tk.Menu(root)
        self.root = root
        self.root.title("Cold Laboratory")
        self.root.config(menu=self.menubar)

        self.modify_root_geometry()
        self.create_measurement_menu()
        self.create_calibration_menu()
        self.create_help_menu()
        
        
        

    def modify_root_geometry(self):
        self.root.geometry("600x600")
        self.root.title("COLD Laboratory")
        self.root.resizable(height=None, width= None)
        self.bg = tk.PhotoImage(file="C:/Users/cold/Documents/ProveQucodes/driver_LNF/Logo-COLD-lab.png")
        self.root.configure(background="white")
        self.bg_label=tk.Label((self.root),image=self.bg)
        self.bg_label.place(relwidth=1, relheight=1)


    def National_instrument():
        pass

    def RS_SMA100B_instrument():
        pass

    def RS_SGS100A_instrument():
        pass
    def Signal_Hound_instrument():
        pass

    def Agilent_33XXX_instrument():
        pass

    def IQ_measurement():
        pass
    def meas_2_measurement():
        pass
    def meas_3_measurement():
        pass


    def configuration_1():
        pass
    def configuration_2():
        pass

    def start_measurement():
        text ="Start"
        text_output = tk.Label(root, text=text, fg="black", font=("Helvetica", 16))
        text_output.grid(row=0, column=1,padx=50, sticky="W")

    def stop_measurement():
        text = "Stop!"
        text_output = tk.Label(root, text=text, fg="green", font=("Helvetica", 16))
        text_output.grid(row=1, column=1, padx=50, sticky="W")


    def gateset_calib():
        pass

    def QB_1():
        pass

    def std_randomized_benchmarking():
        print("Std randomized benchmarking")
        pass
    #--------- low level characterization single qubit
    def rabi_oscillation():
        pass
    def T12():
        pass

    def single_shot_class():
        pass
    def AllXY_DragPulseTraining():
        pass

    def flipping():
        pass

    def dispersive_shift():
        pass

    def readout_fr_optimization():
        pass

    def fast_rst_test():
        pass

    def ToF_readout():
        pass

    def resonator_spec():
        pass
    
    def resonator_po():
        pass
    def resonator_flux_dependance():
        pass

    def qubit_spec():
        pass

    def qubit_flux_dependance():
        pass
    def ramsey_std():
        pass

    def ramsey_detuned():
        pass
    """  
            self.entry = tk.Entry(root)
            self.entry.pack()
            self.input_button =tk.Button(root, text='Get Input',command=self.get_input)
            self.input_button.pack()
            self.result_label =tk.Label(root,text="")
            self.result_label.pack()
    """
    

    def fidelity(self):
        
        self.open_window()
        self.submit_parameters()
        pass

    def QNDness(self):
        from tkinter.simpledialog import askstring
        self.result = askstring("Input", "Enter something:")
        if self.result:
            self.result_label = tk.Label(text="")
            self.result_label.pack()
            self.result_label.config(text=f"You entered: {self.result}")
       
        pass


    def help_menu():
        pass

    def open_window(self):
        self.new_window = tk.Toplevel(root)
        self.new_window.title("Low level: RO characterization, Fidelity")
        self.new_window.geometry("500x400")
        self.label = tk.Label(self.new_window, text="This is a measurement session.")
        self.label.pack(pady=10)

        self.frame2 = tk.Frame(self.new_window)
        self.frame2.pack()

        """self.entry_label = tk.Label(self.frame2,text= "enter something: ")
        self.entry_label.pack()   
        self.entry= tk.Entry(self.frame2)
        self.entry.pack()"""

        self.frame3 = tk.Frame(self.new_window)
        self.frame3.pack()
        self.list_label = tk.Label(self.frame3,text="List", font=("Times New Roman",12))
        # self.list_label.grid(sticky='W')

        self.listbox=tk.Listbox(self.frame3)
        for item in ["item 1 ","item2 ","item 3 ","item 4 "]:
            self.listbox.insert(tk.END,item)
        self.list_label.grid(sticky='W')
        #self.listbox.pack()
        
    def create_help_menu(self):
        self.help_menu = tk.Menu(self.menubar,tearoff=0)
        self.help_menu.add_command(label="Help",command=self.help_menu)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="Help",menu=self.help_menu)

    def create_measurement_menu(self):
        # self.menubar = tk.Menu(root)
        self.measurement_menu = tk.Menu(self.menubar, tearoff=0)
        self.measurement_menu.add_command(label="national", command=self.National_instrument)
        self.measurement_menu.add_command(label="RS_SMA100B", command=self.RS_SMA100B_instrument)
        self.measurement_menu.add_command(label="RS_SGS100A", command=self.RS_SGS100A_instrument)
        self.measurement_menu.add_command(label="RS_SGS100A", command=self.Signal_Hound_instrument)
        self.measurement_menu.add_command(label="Agilent", command=self.Agilent_33XXX_instrument) 
        self.measurement_menu.add_separator()
        self.measurement_menu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="Instrument", menu=self.measurement_menu)


        measurement_menu = tk.Menu(self.menubar, tearoff=0)
        measurement_menu.add_command(label="IQ", command=self.IQ_measurement)
        measurement_menu.add_command(label="meas_2", command=self.meas_2_measurement)
        measurement_menu.add_command(label="meas_3", command=self.meas_3_measurement)
        measurement_menu.add_separator()
        measurement_menu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="Measurement", menu=measurement_menu)

        measurement_submenu = tk.Menu(measurement_menu)
        measurement_submenu.add_command(label="conf_1",command=self.configuration_1)
        measurement_submenu.add_command(label="conf_2",command=self.configuration_2)

        measurement_menu.add_cascade(label="IQ",menu=measurement_submenu)
        """measurement_submenu = tk.Menu(measurement_menu)
        measurement_submenu.add_command(label='conf_1',command= configuration_1)
        measurement_menu.add_cascade(label="IQ",menu=measurement_menu)"""


    def create_calibration_menu(self): 
        # self.menubar = tk.Menu(root)
        self.calibration_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Calibration",menu=self.calibration_menu)
        self.calibration_submenu = tk.Menu(self.calibration_menu)
        self.calibration_menu.add_cascade(label="Sigle Qubit", menu=self.calibration_submenu)

        self.calibration_subsubmenu_gateset = tk.Menu(self.menubar,tearoff=0)
        self.calibration_subsubmenu_gateset.add_command(label ="Std randomized benchmarking", command=self.std_randomized_benchmarking )
        self.calibration_submenu.add_cascade(label="Gate set",menu=self.calibration_subsubmenu_gateset)

        self.calibration_subsubmenu_lowlevel = tk.Menu(self.menubar,tearoff=0)
        self.calibration_subsubmenu_lowlevel.add_command(label ="Rabi oscillation", command= self.rabi_oscillation)
        self.calibration_subsubmenu_lowlevel.add_command(label ="T1 & T2", command= self.T12)
        self.calibration_subsubmenu_lowlevel.add_command(label ="single shot classification", command=self.single_shot_class)
        self.calibration_subsubmenu_lowlevel.add_command(label ="AllXY DragPulseTraining", command=self.AllXY_DragPulseTraining)
        self.calibration_subsubmenu_lowlevel.add_command(label ="Flipping", command=self.flipping)
        self.calibration_subsubmenu_lowlevel.add_command(label ="Dispersive shift", command=self.dispersive_shift)
        self.calibration_subsubmenu_lowlevel.add_command(label ="Readout frequency optimization", command=self.readout_fr_optimization)
        self.calibration_subsubmenu_lowlevel.add_command(label ="Fast reset test", command=self.fast_rst_test)
        self.calibration_subsubmenu_lowlevel.add_command(label ="Time of Flight readout", command=self.ToF_readout)
        self.calibration_submenu.add_cascade(label="Low level",menu=self.calibration_subsubmenu_lowlevel)

        #3lvl
        self.calibration_subsubsubmenu_lowlevel_resch = tk.Menu(self.menubar,tearoff=0)
        self.calibration_subsubsubmenu_lowlevel_resch.add_command(label="Resonator Spectroscopy", command=self.resonator_spec)
        self.calibration_subsubsubmenu_lowlevel_resch.add_command(label="Resonator Punchout", command=self.resonator_po)
        self.calibration_subsubsubmenu_lowlevel_resch.add_command(label="Resonator flux dependance", command=self.resonator_flux_dependance)
        self.calibration_subsubmenu_lowlevel.add_cascade(label="Resonator Characterization",menu=self.calibration_subsubsubmenu_lowlevel_resch)

        self.calibration_subsubsubmenu_lowlevel_quch = tk.Menu(self.menubar,tearoff=0)
        self.calibration_subsubsubmenu_lowlevel_quch.add_command(label="Qubit Spectroscopy", command=self.qubit_spec)
        self.calibration_subsubsubmenu_lowlevel_quch.add_command(label="Qubit flux dependance", command=self.qubit_flux_dependance)
        self.calibration_subsubmenu_lowlevel.add_cascade(label="Qubit Characterization",menu=self.calibration_subsubsubmenu_lowlevel_quch)


        self.calibration_subsubsubmenu_lowlevel_ramsey = tk.Menu(self.menubar,tearoff=0)
        self.calibration_subsubsubmenu_lowlevel_ramsey.add_command(label="Standard", command=self.ramsey_std)
        self.calibration_subsubsubmenu_lowlevel_ramsey.add_command(label="Detuned", command=self.ramsey_detuned)
        self.calibration_subsubmenu_lowlevel.add_cascade(label="Ramsey",menu=self.calibration_subsubsubmenu_lowlevel_ramsey)

        self.calibration_subsubsubmenu_lowlevel_roch = tk.Menu(self.menubar,tearoff=0)
        self.calibration_subsubsubmenu_lowlevel_roch.add_command(label="Fidelity", command=self.fidelity)
        self.calibration_subsubsubmenu_lowlevel_roch.add_command(label="QNDness", command=self.QNDness)
        self.calibration_subsubmenu_lowlevel.add_cascade(label="Readout Characterization",menu=self.calibration_subsubsubmenu_lowlevel_roch)


#---------------
    def submit_parameters(self):
        self.parameter_entries = {}
        for parameter, entry in self.parameter_entries.items():
            self.value = entry.get()
            print(f"{parameter}: {self.value}")      
        #self.parameter_entries = {}
        self.parameters = ["Parameter_1", "Parameter_2", "Parameter_3", "Parameter_4"]
        for parameter in self.parameters:
            self.label = tk.Label(self.new_window, text=parameter)
            self.label.pack()
            self.entry = tk.Entry(self.new_window)
            self.entry.pack()
            self.parameter_entries[parameter] = self.entry
            pass
        self.submit_button = tk.Button(self.new_window, text="Submit", command=self.print_parameters)
        self.submit_button.pack()

   
    df= pd.DataFrame(columns=['parameter'])
    def print_parameters(self):  
        self.parameter_saved=[]
        self.value_saved=[]

        for parameter, entry in self.parameter_entries.items():
            self.value = entry.get()
            self.parameter_saved.append(parameter)
            self.value_saved.append(self.value)
      
        self.df['parameter'] = self.parameter_saved
        

        self.new_column_name = f'value_{len(self.df.columns) - 1}'
        self.df[self.new_column_name] = self.value_saved

        self.df.to_csv("C:/Users/cold/Documents/ProveQucodes/driver_LNF/dataframe.csv")
           
#----------
    """
    first_button = tk.Button(text="Start measurement", command=start_measurement)
    first_button.grid(row=0, column=0, sticky="W")

    second_button = tk.Button(text="Stop measurement", command=stop_measurement)
    second_button.grid(row=1, column=0, pady=20, sticky="W")
    """

if __name__ == "__main__":
    root = tk.Tk() 
    cold_app = ColdLab(root)
    root.mainloop() 