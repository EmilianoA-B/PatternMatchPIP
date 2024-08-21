import csv
from matplotlib import pyplot as plt
from datetime import datetime
import pprint

class grafica:
    def __init__(self):
        self.pendMax =[]
        self.pendMin = []

def leerCSV(pathCSV:str, intervalo:int):
    if pathCSV == "":                   #sin archivo
        print("Ningún archivo detectado")
    elif not pathCSV.endswith('.csv'):  #archivo que no es csv 
        print("Elije un archivo CSV")
    else:                               #archivo csv
        lim_fil = 50000
        intervalo = intervalo/5 #Dividimos el intervalo entre 5, para que queden en saltos de 1,2,3 y 6
        listaDeVal = {}
        with open(pathCSV) as archCSV:
            lector = csv.reader(archCSV)
            next(lector)
            for i,fila in enumerate(lector):
                if i >= lim_fil :
                    break
                elif i%intervalo == 0:
                    listaDeVal[int(i//intervalo)] = float(fila[1])
                else: 
                    continue
        #Graficar     
        datos = sorted(listaDeVal.items())
        #pprint.pprint(datos)
        x,y = zip(*datos)
        plt.cla()
        plt.plot(x,y)
        plt.savefig("graph.png")

        #Encontrar picos y valles
        picos = []
        valles = []
        
        if datos[0][1] > datos[1][1]:
            picos.append(datos[0])
        elif datos[0][1] < datos[1][1]:
            valles.append(datos[0])
        
        for i in range(1,len(datos)-1):
            if datos[i][1] > datos[i-1][1] and datos[i][1] > datos[i+1][1]:
                picos.append(datos[i])
            elif datos[i][1] < datos[i-1][1] and datos[i][1] < datos[i+1][1]:
                valles.append(datos[i])  
                
        if datos[-1][1] > datos[-2][1]:
            picos.append(datos[-1])
        elif datos[-1][1] < datos[-2][1]:
            valles.append(datos[-1])
         
        #Usamos solo los 3 valores más pronunciados para maximos y mínimos
        picos = sorted(picos, key= lambda data: data[1], reverse=True)[:3]
        valles = sorted(valles, key=lambda data: data[1], reverse=True)[:3]
        
        picos.sort(key= lambda data: data[0])
        valles.sort(key= lambda data: data[0])
        
        print("picos",picos)
        print("valles", valles)
        #Pendiente
        grafCSV = grafica()
        
        for i in range(len(picos)-1):
            pendiente = (picos[i+1][1] - picos[i][1])/(picos[i+1][0] - picos[i][0])
            grafCSV.pendMax.append(pendiente)
            
        print("Pendientes de maxs",grafCSV.pendMax)

        for i in range(len(valles)-1):
            pendiente = (valles[i+1][1] - valles[i][1])/(valles[i+1][0] - valles[i][0])
            grafCSV.pendMin.append(pendiente)
            
        print("Pendientes de mins",grafCSV.pendMin)
        
        