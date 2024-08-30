from tkinter import * 
from tkinter import ttk 
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
from analizarCSV import *
class patronesGUI:
    def __init__(self, root): #Inicializacion de GUI
        self.archivoSeleccionado = ""
        self.intervalos = 5  #Valor default de 5 min
        root.title("Ejercicio Arcode")
        self.interfaz = ttk.Frame(root, padding="3 3 3 3")
        self.interfaz.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        botonParaImportarCSV = ttk.Button(self.interfaz, text="Abrir CSV",command=self.getArchivoName)
        botonParaImportarCSV.grid(row=1,column=1,sticky=(S,W))

        botonParaSalir = ttk.Button(self.interfaz, text="Salir", command=quit)
        botonParaSalir.grid(row=1,column=4, sticky=(S,E))

        opcionesDeIntervalos = [5,10,15,30]
        intervalos = IntVar()
        intervalos.set(opcionesDeIntervalos[0])

        textoIntervalos = Label(self.interfaz, text="Intervalos:")
        textoIntervalos.grid(row=1,column=2,sticky=(S))

        menuIntervalos = OptionMenu(self.interfaz,intervalos,*opcionesDeIntervalos,command=self.getIntervalos)
        menuIntervalos.grid(row=1,column=3,sticky=(S))

        botonParaIniciar = ttk.Button(self.interfaz, text="Analizar Datos", command=self.empezarAnalisis)
        botonParaIniciar.grid(row=2,column=1)

        for child in self.interfaz.winfo_children():
            child.grid_configure(padx=5,pady=5)
            
    def getArchivoName(self, event=None): 
        self.archivoSeleccionado = filedialog.askopenfilename()
    
    def getIntervalos(self, seleccion):
        self.intervalos = seleccion
        print("estos son los intervalos",self.intervalos)
    
    def empezarAnalisis(self):
        patron = leerCSV(self.archivoSeleccionado,self.intervalos)
        if patron == 0:
            self.viewGrafica()
            print("Ningun patron se reconocio")
            self.popUp("Ningun patrón se reconoció")
        elif patron == None:
            print("Intenta otra vez")
            self.popUp("Intenta otra vez")
        else:
            self.viewGrafica()
            msg = "Se encontró similitud con el patrón #" + str(patron)
            print(msg)   
            self.popUp(msg)
            
    def popUp(self,msg:str):
        messagebox.showinfo(message=msg)
        
    def viewGrafica(self):
        graph = Image.open("graph.png")
        graph = graph.resize((800,500), Image.Resampling.LANCZOS)
        graph = ImageTk.PhotoImage(graph)
        grafica = Label(self.interfaz, image=graph)
        grafica.image = graph
        grafica.grid(padx=5, pady=5, row=0,column=1,columnspan=4)
        

root = Tk()
patronesGUI(root)
root.mainloop()
