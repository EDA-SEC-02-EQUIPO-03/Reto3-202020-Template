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
import calendar
import math

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
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    analyzer['Geographic'] = om.newMap(omaptype='BST',
                                      comparefunction=compareGeo)
    return analyzer

# Funciones para agregar informacion al catalogo

def addaccident(analyzer, accidents):
    """
    """
    lt.addLast(analyzer['accidents'], accidents)
    #lt.addFirst(analyzer['accidents'], accidents)
    updateDateIndex(analyzer['dateIndex'], accidents)
    updateGeographic(analyzer['Geographic'], accidents)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
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

def updateGeographic(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    Lat = accident['Start_Lat']
    Long= accident['Start_Lng']
    key=(Long,Lat)
    entry = om.get(map, key)
    if entry == None:
        lst=lt.newList()
    else:
        lst=me.getValue(entry)
    lt.addLast(lst,accident)
    #lt.addFirst(lst,accident)
    
    om.put(map, key, lst)
    
    #addDateIndex(datentry, accident)
    return map


# def addDateIndex(datentry, accident):
#     """
#     Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
#     de crimenes y una tabla de hash cuya llave es el tipo de crimen y
#     el valor es una lista con los crimenes de dicho tipo en la fecha que
#     se está consultando (dada por el nodo del arbol)
#     """
#     lst = datentry['lstaccident']
#     lt.addLast(lst, accident)
#     offenseIndex = datentry['offenseIndex']
#     offentry = m.get(offenseIndex, crime['OFFENSE_CODE_GROUP'])
#     if (offentry is None):
#         entry = newOffenseEntry(crime['OFFENSE_CODE_GROUP'], crime)
#         lt.addLast(entry['lstoffenses'], crime)
#         m.put(offenseIndex, crime['OFFENSE_CODE_GROUP'], entry)
#     else:
#         entry = me.getValue(offentry)
#         lt.addLast(entry['lstoffenses'], crime)
#     return datentry

def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstaccidents': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry

# ==============================
# Funciones de consulta
# ==============================

def keyset(map):
    return m.keySet(map)

def getaccident(tree,key):
    return me.getValue(om.get(tree,key))
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

def compareGeo(geo1,geo2):
    if geo1[0]==geo2[0] and geo1[1]==geo2[1]:
        return 0
    elif geo1[0]>geo2[0] or geo1[1]>geo2[1]:
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

def getStateMoreAccidentsByRange(analyzer,initialDate, finalDate):
    Estados={}
    info=om.values(analyzer['dateIndex'],initialDate,finalDate)
    for j in range(1,lt.size(info)+1):
            it1=lt.getElement(info,j)
            for i in range(1,lt.size(it1)+1):
                it2=lt.getElement(it1,i)
                estado=it2['State']
                if estado in Estados:
                    Estados[estado]+=1
                else:
                    Estados[estado]=1
    big=0
    for k in Estados.keys():
        value=Estados[k]
        if value>big:
            big=value
            res=k
    return res 

def getDateMoreAccidentsByRange(analyzer,initialDate, finalDate):
    keys=om.keys(analyzer['dateIndex'],initialDate, finalDate)
    value=""
    if not lt.isEmpty(keys):
        big=0
        for i in range(1,lt.size(keys)+1):
            key=lt.getElement(keys, i)
            accidentdate=getaccident(analyzer['dateIndex'],key)
            size=lt.size(accidentdate)
            if size>big:
                big=size
                value=key
    return value

def dayOfTheWeek(date): #"YYYY-MM-DD"
    year=date[:4]
    month=date[5:7]
    day=date[8:10]
    theDate=day+" "+month+" "+year
    born = datetime.datetime.strptime(theDate, '%d %m %Y').weekday() 
    n=(calendar.day_name[born]) 
    if n.lower()=="monday":
        day="Lunes"
    elif n.lower()=="tuesday":
        day="Martes"
    elif n.lower()=="wednesday":
        day="Miércoles"
    elif n.lower()=="thursday":
        day="Jueves"
    elif n.lower()=="friday":
        day="Viernes"
    elif n.lower()=="saturday":
        day="Sábado"
    elif n.lower()=="sunday":
        day="Domingo"
    else:
        day="Fecha incorrecta"
    return day


def getDistanceBetweenCenterAndPoint(LatC,LongC,LatP,LongP):
    degree_to_mile=24901.92/360
    NewLatC=LatC*degree_to_mile
    NewLongC=LongC*degree_to_mile
    NewLatP=float(LatP)*degree_to_mile
    NewLongP=float(LongP)*degree_to_mile
    a=(NewLongP-NewLongC)**2
    b=(NewLatP-NewLatC)**2
    c=a+b
    distance=math.sqrt(c)
    return distance


#def getDateofLatLong(lst):
    #for g in range(1,lt.size(lst)+1):
                        #accidents_geo1=lt.getElement(lst,g)
                        #for p in range(1,lt.size(accidents_geo1)+1):
                            #accidents_geo2=lt.getElement(accidents_geo1,p)
                            #date=accidents_geo2['Start_Time'][:10]
    #return date


def getAccidentsGeographicalArea (analyzer,LatC,LongC,radio):
    dayAccidents={}
    info=om.valueSet(analyzer['Geographic'])
    for j in range(1,lt.size(info)+1):
            it1=lt.getElement(info,j)
            for i in range(1,lt.size(it1)+1):
                it2=lt.getElement(it1,i)
                Lat=it2['Start_Lat']
                Long=it2['Start_Lng']
                date=it2['Start_Time'][:10]
                distance=getDistanceBetweenCenterAndPoint(LatC,LongC,Lat,Long)
                if distance<=radio:
                    day=dayOfTheWeek(date)
                    if day in dayAccidents:
                            dayAccidents[day]+=1
                    else:
                            dayAccidents[day]=1
    return dayAccidents


