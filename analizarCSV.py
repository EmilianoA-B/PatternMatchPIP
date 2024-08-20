import csv
from datetime import datetime
import pprint

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
                    listaDeVal[int(i//intervalo)] = fila[1]
                else: 
                    continue
            pprint.pprint(listaDeVal)
