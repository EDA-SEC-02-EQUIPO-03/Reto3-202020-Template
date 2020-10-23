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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m

import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None,
                'hourIndex': None,
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['hourIndex'] = om.newMap(omaptype='RBT',comparefunction=compareHour)
    return analyzer

# Funciones para agregar informacion al catalogo

def addaccident(analyzer, accidents):
    """
    """
    lt.addLast(analyzer['accidents'], accidents)
    #lt.addFirst(analyzer['accidents'], accidents)
    updateDateIndex(analyzer['dateIndex'], accidents)
    updateHourIndex(analyzer['hourIndex'],accidents)
    return analyzer

def updateDateIndex(map, accident):
    
    accidentdate = accident['Start_Time'][:10]
    
    entry = om.get(map, accidentdate)
    if entry == None:
        lst=lt.newList()
    else:
        lst=me.getValue(entry)
    lt.addLast(lst,accident)
    #lt.addFirst(lst,accident)

    om.put(map, accidentdate, lst)
    
    #addDateIndex(datentry, accident)
    return map

def updateHourIndex(map,accident):

    accidenthour = 60*int(accident['Start_Time'][11:13])
    
    accidentmin = int(accident['Start_Time'][14:16])
    accidentminround = (accidentmin//30)*30
    time=accidenthour+accidentminround
    
    entry = om.get(map,time)
    if entry == None:
        lst=lt.newList()
    else:
        lst=me.getValue(entry)
        
    lt.addLast(lst,accident)
    
    
    om.put(map, time, lst)
    return map




# ==============================
# Funciones de consulta
# ==============================

def keyset(map):
    return m.keySet(map)

def getaccident(tree,key):
    return me.getValue(om.get(tree,key))

def getaccidentrange(analyzer,minkey,maxkey):
    accidentsdate=analyzer['dateIndex']
    dates= om.values(accidentsdate,minkey,maxkey)
    categoria=lt.newList()
    categoriamax=None
    lt.addLast(categoria,0)
    lt.addLast(categoria,0)
    lt.addLast(categoria,0)
    lt.addLast(categoria,0)
    
    cantidad=0
    for i in range(1,lt.size(dates)+1):
        fecha=lt.getElement(dates,i)
        for a in range(1,lt.size(fecha)+1):
            cantidad += 1
            accidente=lt.getElement(fecha,a)
            severidad=int(accidente['Severity'])
            value=lt.getElement(categoria,severidad)
            lt.insertElement(categoria, value+1,severidad)
            if cantidad==1:
                categoriamax=severidad 
            elif value+1>lt.getElement(categoria,categoriamax):
                categoriamax=severidad
                
    return categoria,cantidad,categoriamax

def getaccidenthourrange (analyzer,minkey,maxkey):
    accidentshour=analyzer['hourIndex']
    mintime = (60*int(minkey[0:2]))+int(minkey[3:5])
    maxtime = (60*int(maxkey[0:2]))+int(maxkey[3:5])
    #print(mintime,maxtime)
    #prueba
    #print(om.get(accidentshour,720))
    
    hours= om.values(accidentshour,mintime,maxtime)
    
    categoria=lt.newList()
    lt.addLast(categoria,0)
    lt.addLast(categoria,0)
    lt.addLast(categoria,0)
    lt.addLast(categoria,0)
    cantidad=0
    for i in range(1,lt.size(hours)+1):
        hora=lt.getElement(hours,i)
        
        for a in range(1,lt.size(hora)+1):
            cantidad += 1
            accidente=lt.getElement(hora,a)
            severidad=int(accidente['Severity'])
            valor=lt.getElement(categoria,severidad)
            lt.insertElement(categoria,valor+1,severidad)
   
    return categoria,cantidad




    

# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
   
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

def crimesSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])


def getCrimesByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    return lst


def getCrimesByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = om.get(analyzer['dateIndex'], initialDate)
    if crimedate['key'] is not None:
        offensemap = me.getValue(crimedate)['offenseIndex']
        numoffenses = m.get(offensemap, offensecode)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstoffenses'])
        return 0


# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareHour(hour1,hour2):
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1

def compareOffenses(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
def size(analyzer):
    return om.size(analyzer)