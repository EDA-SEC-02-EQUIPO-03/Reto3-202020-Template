"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config
import time 

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = 'us_accidents_dis_2016.csv'

# _________________________________________________us_accidents_small.csv__
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 4")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        t1=time.process_time()
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfile)
        print('Crimenes cargados: ' + str(controller.crimesSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        t2=time.process_time()
        print(t2-t1)

    elif int(inputs[0]) == 3:
        date = input('Por favor ingrese la fecha de la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        print("\nRequerimiento No 1 del reto 3: ")
        accidents_in_date = lt.size(controller.getAccident(cont['dateIndex'],date))
        print("la cantidad de accidentes el ",date,"son ",accidents_in_date)


    elif int(inputs[0]) == 4:
        t1=time.process_time()
        print("\nRequerimiento No 4 del reto 3: ")
        datelo = input('Por favor ingrese la fecha inicial desde la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        datehi = input('Por favor ingrese la fecha final desde  la cuál desea buscar los accidentes: (YYYY-MM-DD)\n')
        mas_accidentes_fecha= controller.getDateMoreAccidentsByRange(cont,datelo,datehi)
        mas_accidentes_estado=controller.getStateMoreAccidentsByRange(cont,datelo,datehi)
        print( "El estado con mas accidentes entre ",datelo," y ",datehi," es: ",mas_accidentes_estado)
        print("La fecha con mas accidentes entre ",datelo," y ",datehi," es: ",mas_accidentes_fecha)
        t2=time.process_time()
        print(t2-t1)

    else:
        sys.exit(0)
sys.exit(0)
