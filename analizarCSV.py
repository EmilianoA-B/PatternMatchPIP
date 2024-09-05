import csv
from matplotlib import pyplot as plt
from datetime import datetime
import pprint

class grafica:
    def __init__(self):
        self.difsMax = []
        self.difsMin = []

class patron(grafica):
    def __init__(self):
        self.numPatron = 0
        self.puntos = 0
              
    def comparacionPatrones(self, graf:grafica):
        tolerancia = 15 
        if len(self.difsMin) == len(graf.difsMin):
            for i in range(len(self.difsMin)):
                if abs(graf.difsMin[i] - self.difsMin[i]) >= tolerancia:
                    return False 
        else:
            return False
        
        if len(self.difsMax) == len(graf.difsMax):
            for i in range(len(self.difsMax)):
                if abs(graf.difsMax[i] - self.difsMax[i]) >= tolerancia:
                    return False 
        else:
            return False
        return True

    def comprobarPatrones(self,datos):
        puntosX = [0, len(datos) - 1]  # Indice  
        puntosY = [datos[0][1], datos[-1][1]] # Precio
        print("Todos los datos:")
        pprint.pprint(datos)
        
        for curr_point in range(2, self.puntos):

            distancia_max = 0.0 # Distancia maxima
            dist_max_indice = -1 # Distancia
            indice_insert = -1

            for k in range(0, curr_point - 1):

                # Indice para punto izquierdo y indice para punto derecho
                left_adj = k
                right_adj = k + 1

                diff_tiempo = puntosX[right_adj] - puntosX[left_adj]
                diff_precio = puntosY[right_adj] - puntosY[left_adj]
                pendiente = diff_precio / diff_tiempo
                pInterseccion = puntosY[left_adj] - puntosX[left_adj] * pendiente;
                
                for i in range(puntosX[left_adj] + 1, puntosX[right_adj]):
                    
                    distancia = 0.0 # Distancia
                    distancia = abs( (pendiente * i + pInterseccion) - datos[i][1] ) / (pendiente ** 2 + 1) ** 0.5
                    
                    if distancia > distancia_max: #Checar si la distancia actual es mayor que la maxima
                        distancia_max = distancia
                        dist_max_indice = i
                        indice_insert = right_adj

            puntosX.insert(indice_insert, dist_max_indice)
            puntosY.insert(indice_insert, datos[dist_max_indice][1])

        print("Puntos X:",puntosX)
        print("Puntos Y:",puntosY)
        
        picos = []
        valles = []
        i=0
        
        if puntosY[0] < puntosY[1]:
            while i<len(puntosY):
                valles.append(tuple((puntosX[i], puntosY[i])))
                i+=1
                if i<len(puntosY):
                    picos.append(tuple((puntosX[i], puntosY[i])))
                    i+=1
        else:
            while i<len(puntosY):
                picos.append(tuple((puntosX[i], puntosY[i])))
                i+=1
                if i<len(puntosY):
                    valles.append(tuple((puntosX[i], puntosY[i])))
                    i+=1
                    
        print("picos no normalizados",picos)
        print("valles no normalizados",valles)
        
        #Normalizar datos en escala de 0 a 100
        picos, valles = normalizacion(picos,valles)
        
        #Ver valores normalizados
        print("picos normalizados",picos)
        print("valles normalizados",valles)
        
        grafCSV = grafica()
        
        for i in range(len(picos)-1):
            grafCSV.difsMax.append(picos[i] - picos[i+1])
            
        for i in range(len(valles)-1):
            grafCSV.difsMin.append(valles[i] - valles[i+1])   
        
        #Ver difs
        print("difs max",grafCSV.difsMax)
        print("difs min",grafCSV.difsMin)
        
        return self.comparacionPatrones(grafCSV)
        

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
        x,y = zip(*datos)
        plt.cla()
        plt.plot(x,y)
        plt.savefig("graph.png")
        
        #Valores de patrones
        patrones = []
        
        patron1 = patron()
        patron1.difsMax = [25, 15]
        patron1.difsMin = [-25]
        patron1.numPatron = 1
        patron1.puntos = 5
        patrones.append(patron1)
        
        patron2 = patron()
        patron2.difsMax = [0, 0]
        patron2.difsMin = [-50]
        patron2.numPatron = 2
        patron2.puntos = 5
        patrones.append(patron2)
        
        patron3 = patron()
        patron3.difsMax = [0, 0]
        patron3.difsMin = [50, -50]
        patron3.numPatron = 3
        patron3.puntos = 6
        patrones.append(patron3)
        
   
        for i in range(len(patrones)):
            patIterator = patrones[i]
            if patIterator.comprobarPatrones(datos):
                return patIterator.numPatron
                
        return 0

#Función de normalización
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
    