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

    om.put(map, accidentdate, lst)
    
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



def getAccidentsGeographicalArea (analyzer,LatC,LongC,radio):
    dayAccidents={}
    info=om.valueSet(analyzer['dateIndex'])
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


def size(analyzer):

    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):

    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):

    return om.size(analyzer['dateIndex'])


def minKey(analyzer):

    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):

    return om.maxKey(analyzer['dateIndex'])





