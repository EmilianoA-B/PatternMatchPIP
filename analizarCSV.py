import csv
from matplotlib import pyplot as plt
from datetime import datetime
import pprint

class grafica:
    def __init__(self):
        self.difsMax =[]
        self.difsMin = []

def leerCSV(pathCSV:str, intervalo:int):
    if pathCSV == "":                   #sin archivo
        print("Ningún archivo detectado")
        return None
    elif not pathCSV.endswith('.csv'):  #archivo que no es csv 
        print("Elije un archivo CSV")
        return None
    else:                               #archivo csv
        print("---------------Analisis-----------------")
        lim_fil = 50000
        intervalo = intervalo//5 #Dividimos el intervalo entre 5, para que queden en saltos de 1,2,3 y 6
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
        
        #Si uno de los valles es 0 mantenemos los 3 datos valles, si no, nos quedamos con 2 
        flagForZero = False
        for v in valles:
            if 0 == v[0]:
                flagForZero = True
        if flagForZero == False:
            valles = valles[:2]
        valles.sort(key= lambda data: data[0])
        
        #Ver los picos y valles
        print("picos",picos)
        print("valles",valles)
        
        #Normalizacion de valores
        picos, valles = normalizacion(picos,valles)
        
        #Ver valores normalizados
        print("picos normalizados",picos)
        print("valles normalizados",valles)
        
        #Calculo de diferencias
        grafCSV = grafica()
        
        for i in range(len(picos)-1):
            grafCSV.difsMax.append(picos[i] - picos[i+1])
            
        for i in range(len(valles)-1):
            grafCSV.difsMin.append(valles[i] - valles[i+1])   
        
        #Ver difs
        print("difs max",grafCSV.difsMax)
        print("difs min",grafCSV.difsMin)
        
        #Valores de patrones TODO: Calcular difs en patrones
        patrones = []
        
        patron1 = grafica()
        patron1.difsMax = [25, 15]
        patron1.difsMin = [-25]
        patrones.append(patron1)
        
        patron2 = grafica()
        patron2.difsMax = [0, 0]
        patron2.difsMin = [-50]
        patrones.append(patron2)
        
        patron3 = grafica()
        patron3.difsMax = [0, 0]
        patron3.difsMin = [50, -50]
        patrones.append(patron3)
        
        for i in range(3):
            patrones[i]
            if comparacionPatrones(patrones[i], grafCSV):
                return i+1
        return 0

        
#Funcion de comparacion        
def comparacionPatrones(patron:grafica, graf:grafica):
    tolerancia = 15 #Tolerancia del 15%
    if len(patron.difsMin) == len(graf.difsMin):
        for i in range(len(patron.difsMin)):
            if abs(graf.difsMin[i] - patron.difsMin[i]) >= tolerancia:
                return False 
    else:
        return False
    
    if len(patron.difsMax) == len(graf.difsMax):
        for i in range(len(patron.difsMax)):
            if abs(graf.difsMax[i] - patron.difsMax[i]) >= tolerancia:
                return False 
    else:
        return False
    return True

def normalizacion(maximos, minimos):
    auxMinimos = []
    auxMaximos = []
    maxVal = max(maximos, key=lambda val: val[1])[1]
    minVal = min(minimos, key=lambda val: val[1])[1]
    denom = maxVal - minVal
    if denom == 0: #Si el rango de valores es de 0 a 0
        return [0],[0]
    
    for i in range(len(maximos)): #Normalizar maximos
        nom = maximos[i][1] - minVal
        auxMaximos.append((nom/denom)*100)
        
    for i in range(len(minimos)): #Normalizar minimos
        nom = minimos[i][1] - minVal
        auxMinimos.append((nom/denom)*100)
    return auxMaximos, auxMinimos
    