from tkinter import * 
from tkinter import ttk 
from tkinter import filedialog
from analizarCSV import *
class patronesGUI:
    def __init__(self, root):
        self.archivoSeleccionado = ""
        self.intervalos = 5  #Valor default de 5 min
        root.title("Ejercicio Arcode")
        interfaz = ttk.Frame(root, padding="3 3 3 3")
        interfaz.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        botonParaImportarCSV = ttk.Button(interfaz, text="Abrir CSV",command=self.getArchivoName)
        botonParaImportarCSV.grid(row=1,column=1,sticky=(S,W))

        botonParaSalir = ttk.Button(interfaz, text="Salir", command=quit)
        botonParaSalir.grid(row=1,column=4, sticky=(S,E))

        opcionesDeIntervalos = [5,10,15,30]
        intervalos = IntVar()
        intervalos.set(opcionesDeIntervalos[0])

        textoIntervalos = Label(interfaz, text="Intervalos:")
        textoIntervalos.grid(row=1,column=2,sticky=(S))

        menuIntervalos = OptionMenu(interfaz,intervalos,*opcionesDeIntervalos,command=self.getIntervalos)
        menuIntervalos.grid(row=1,column=3,sticky=(S))

        botonParaIniciar = ttk.Button(interfaz, text="Analizar Datos", command=self.empezarAnalisis) #To do: insert function to run analysis
        botonParaIniciar.grid(row=2,column=1)

        for child in interfaz.winfo_children():
            child.grid_configure(padx=5,pady=5)
            
    def getArchivoName(self, event=None):
        self.archivoSeleccionado = filedialog.askopenfilename()
    
    def getIntervalos(self, seleccion):
        self.intervalos = seleccion
        print("estos son los intervalos",self.intervalos)
    
    def empezarAnalisis(self):
        leerCSV(self.archivoSeleccionado,self.intervalos)

root = Tk()
patronesGUI(root)
root.mainloop()
