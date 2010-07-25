#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

print "Fpl Charge =) "

import Convertion, os, re
from usualFonction import *
from time import gmtime, strftime
from datetime import datetime, timedelta

fpl = {}     # dictionary of fpl : { (x) : instance}
ETX = chr(3)
FPL = re.compile("""\
\(FPL- *(.+?) *- *(.+?) *- *(.+?) *- *(.+?) *- *([A-Z]{4}[0-9]{4}).*- *([KNM][\
0-9]{3,4}([FSA]|VFR)[0-9]{0,4}) (.+?) *- *([A-Z]{4}[0-9]{4}).*-(.*?) *(\)|$)\
""")
    
class Fpl (object):
    
    log = ''
    def __init__(self, donnees, date, points, routes, airport):
        """
        # Creation of a new route
        #
        # definition of variables :
        #
        # self.name = str        is the name of route
        # self.sense = str        is the sens of route
        # self.odds = str        ODDS/EVENS or NONE
        # self.points = []         is the list of points of the route
         """
        self.defPoints       = points
        self.defRoutes       = routes
        self.defAirport      = airport
        self.description     = donnees
        self.messageTime     = date
        self.points          = {}
        self.altitude        = {}
        self.speed           = {}
        self.name            = ''
        self.trajectTime     = {}
        self.deparatureTime  = datetime(2000,1,1)
        self.estimatedTime   = timedelta(0)
        self.flightStatus    = ''

        self.definition(donnees)
        # Add a fpl at the dictionary
        if str(self.name) in fpl :
            del fpl[str(self.name)]
            
        fpl[str(self.name)] = self

    def definition (self, donnees) :
        """ 
        # The data arrives in this form:
        # (FPL-.......) 
        #
        #  FPL
        #   |   Aircraft Identification 
        #   |     |   Flight Rules and Type of flight
        #   |     |     |  Type of Aircraft / Wake Turbulence Category
        #   |     |     |     |   Radio Communication, Navigation and
        #   |     |     |     |   Approach Aid Equipment / Surveillance 
        #   |     |     |     |   Equipment
        #   |     |     |     |     |  Departure Aerodrome / Time
        #   |     |     |     |     |     | Point, Routes ...
        #   |     |     |     |     |     |     |  Destination Aerodrome
        #   |     |     |     |     |     |     |  / Total Estimated 
        #   |     |     |     |     |     |     |  Elapsed Time
        #   |     |     |     |     |     |     |     |   EET ...
        #   |     |     |     |     |     |     |     |     |
        #   V     V     V     V     V     V     V     V     V
        # _____-_____-_____-_____-_____-_____-_____-_____-_____ 
        #
        # The separation will therefore be using the separator "-" and " "
        """
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("-")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        
        # Assigning variables
        if 'FPL' in tabDonnees[0] :
            self.aircraftID = str(tabDonnees[1]) #Aircraft Identification 
            self.flightRulesAndType = str(tabDonnees[2])
            self.aircraftType = str(tabDonnees[3])
            self.equipement = str(tabDonnees[4])
            self.deparatureAerodrome = str(tabDonnees[5][0:4])
            self.dTime = str(tabDonnees[5][4:8])
            self.pointsAndRoutes = tabDonnees[6].split(" ")
            self.destinationAerodrome = str(tabDonnees[7][0:4])
            self.eTime = str(tabDonnees[7][4:8])
            self.comments = tabDonnees[8]
            self.estimatedTime = timedelta(
                hours = int(self.eTime[0:2]), 
                minutes = int(self.eTime[2:])
                )
            self.setDeparatureTime()
            self.addPoints()
            self.setDistance()
            self.addTime()
            self.setFlightPlanStatus()
            self.name = (str(self.aircraftID) +'-'+
                str(self.deparatureAerodrome) + '-' +
                self.deparatureTime.strftime("%Y%m%d-%H%M")
                )
    
    def setFlightPlanStatus(self):
        """
        define with the deparature and arival aerodrome if the flight is :
        in, out, transit or internal.
        """
        if self.deparatureAerodrome in self.defAirport :
            if self.destinationAerodrome in self.defAirport :
                self.flightStatus = 'internal'
            else :
                self.flightStatus = 'out'
        elif self.destinationAerodrome in self.defAirport :
            self.flightStatus = 'in'
        else :
            self.flightStatus = 'transit'
            

    def setDeparatureTime(self):
        dTime = self.dTime
        time= self.messageTime
        if r'DOF/' in self.comments :
            debut = self.comments.find(r'DOF/')
            dof = '20' + self.comments[debut+4:debut+10]
            if dof.isdigit() :
                self.deparatureTime = datetime(
                    int(dof[0:4]),
                    int(dof[4:6]),
                    int(dof[6:]),
                    int(dTime[0:2]),
                    int(dTime[2:])
                    )
                #print self.deparatureTime
            else : 
                Fpl.log += ('DOF error = Flight : ' +
                    self.name + ' - new deparature time :' +
                    str(self.deparatureTime) + '\n')
                    
        if self.deparatureTime.year == 2000 :
            # determines the day of departure from the day and time 
            # the message was sent. the day of departure is the same as 
            # that of sending the following message it was sent within 
            # 2 hours after the departure of the aircraft.
            dTimeMn = int(dTime[0:2])*60 + int(dTime[2:]) # Deparature
            fTimeMn = int(time.hour)*60 + int(time.minute) # Message
            # + 120 min for the 2 hours
            deltaTime= dTimeMn + 120 - fTimeMn
            if deltaTime >= 1440 :
                self.deparatureTime = datetime(
                    time.year,
                    time.month,
                    time.day - 1,
                    int(dTime[0:2]),
                    int(dTime[2:])
                    )
            elif deltaTime < 0 :
                self.deparatureTime = datetime(
                    time.year,
                    time.month,
                    time.day + 1,
                    int(dTime[0:2]),
                    int(dTime[2:])
                    )
            else :
                self.deparatureTime = datetime(
                    time.year,
                    time.month,
                    time.day,
                    int(dTime[0:2]),
                    int(dTime[2:])
                    )
            Fpl.log += ('No DOF = Flight : ' +
                self.name + ' - new deparature time :' +
                str(self.deparatureTime) + '\n')

    def addPoints (self) :
        pointsAndRoutes = self.pointsAndRoutes
        self.listOfPoints=[]
        pointRoute = []
        convert = Convertion.speedAndLevel(pointsAndRoutes[0])
        curentAltitude = convert['altitude']
        curentSpeed = convert['speed']
        self.listOfPoints.append(self.deparatureAerodrome)
        self.altitude[self.deparatureAerodrome] = curentAltitude
        self.speed[self.deparatureAerodrome] = curentSpeed
        #print 'debut: ' + str(pointsAndRoutes[0])
        for x in xrange(1,len(pointsAndRoutes)):
            if "/" in pointsAndRoutes[x]:
                tab = pointsAndRoutes[x].split("/")
                if tab[1] :
                    convert = Convertion.speedAndLevel(tab[1])
                    curentAltitude = convert['altitude']
                    curentSpeed = convert['speed']
                if tab[0] :
                    pointRoute.append(tab[0])
                    self.altitude[tab[0]] = curentAltitude
                    self.speed[tab[0]] = curentSpeed
            else :
                if pointsAndRoutes[x] :
                    pointRoute.append(pointsAndRoutes[x])
                    self.altitude[pointsAndRoutes[x]] = curentAltitude
                    self.speed[pointsAndRoutes[x]] = curentSpeed
        for x in xrange(len(pointRoute)):
            if pointRoute[x] in self.defPoints :
                point = self.defPoints[pointRoute[x]]
                self.listOfPoints.append(point.name)
            elif pointRoute[x] in self.defRoutes :
                route = self.defRoutes[pointRoute[x]]
                curentRouteAltitude = self.altitude[pointRoute[x]]
                curentRouteSpeed = self.speed[pointRoute[x]]
                yDebut = -1
                yFin = -1
                listPoint = []
                for y in xrange(len(route.points)) :
                    if route.points[y] == pointRoute[x-1] :
                        yDebut = y
                    elif route.points[y] == pointRoute[x+1] :
                        yFin = y
                if yDebut == -1 or yFin == -1 :
                    pass
                elif yDebut < yFin :
                    for i in range(yDebut+1, yFin) :
                        point = route.points[i]
                        listPoint.append(point)
                        self.altitude[point] = curentRouteAltitude
                        self.speed[point] = curentRouteSpeed
                    for i in xrange(len(listPoint)) :
                        point = listPoint[i]
                        self.listOfPoints.append(point)
                else :
                    for i in range(yFin+1, yDebut) :
                        point = route.points[i]
                        listPoint.append(point)
                        self.altitude[point] = curentRouteAltitude
                        self.speed[point] = curentRouteSpeed
                    leng = len(self.listOfPoints)
                    for i in xrange(len(listPoint)) :
                        point = listPoint[i]
                        self.listOfPoints.insert(leng, point)
            else :
                self.listOfPoints.append(pointRoute[x])
        self.listOfPoints.append(self.destinationAerodrome)
        self.altitude[self.destinationAerodrome] = curentAltitude
        self.speed[self.destinationAerodrome] = curentSpeed

        i = 0
        for x in xrange(len(self.listOfPoints)):
            point = self.listOfPoints[x]
            if point in self.defPoints :
                defPoint = self.defPoints[self.listOfPoints[x]]
                coordinate = defPoint.decimalCoordinate
                name = defPoint.name
                self.points[i]= {
                    'coordinate' : coordinate,
                    'name' : name,
                    'altitude' : self.altitude[name],
                    'speed' : self.speed[name]
                    }
                i += 1
            elif point == 'DCT' or point == '':
                pass
            else :
                 try :
                    coordinate = Convertion.convertCoordinate(point)
                    name = point
                    self.points[i]= {
                        'coordinate' : coordinate,
                        'name' : name,
                        'altitude' : self.altitude[name],
                        'speed' : self.speed[name]
                        }
                    i += 1
                 except :
                    Fpl.log += ('POINT error = Flight : ' +
                    self.name + '     Point: ' +
                    str(point) + '\n')
        #print self.name
        #if selfprint self.points

    def setDistance (self) :
        """
        Add distance in milles
        """
        # initiate the first point
        self.points[0]['totalDistance'] = 0
        self.points[0]['lastPointDistance'] = 0
        for i in xrange(1,len(self.points)):
            point = self.points[i]
            lastPoint = self.points[i-1]
            ltd = lastPoint['totalDistance']
            distance = Convertion.distanceBetwennTwoPoint(
                point['coordinate']['latitude'],
                point['coordinate']['longitude'],
                lastPoint['coordinate']['latitude'],
                lastPoint['coordinate']['longitude'],
                lastPoint['altitude']
                )
            lpd = distance
            td = ltd + lpd
            point['totalDistance'] = td
            point['lastPointDistance'] = lpd
        #print self.points

    def addTime (self):
        """
        Add time for all point
        """
        # Depending on the estimate of time elapsed
        # Determine the total distance
        totalDistance = self.points[len(self.points)-1]['totalDistance']
        totalTime = self.estimatedTime
        self.points[0]['estimatedTotalTime'] = timedelta(minutes=0)
        self.points[0]['estimatedPointTime'] = timedelta(minutes=0)
        for i in xrange(1,len(self.points)):
            point = self.points[i]
            lastPoint = self.points[i-1]
            distance = point['lastPointDistance']
            lastTime = lastPoint['estimatedTotalTime']
            time = totalTime *int(distance * 1000000000 / totalDistance)
            time = time / 1000000000 
            point['estimatedPointTime'] = time
            point['estimatedTotalTime'] = lastTime + time
        
            #print 'Estimated = Total :' + str(totalTime) + ' time :'+ 
                        #str(time) + ' lastTime :' + str(lastTime + time)
        # Depending on the speed of the aircraft
        # speed is given in miles per hour and the distance in miles
        self.points[0]['calculateTotalTime'] = timedelta(minutes=0)
        self.points[0]['calculatePointTime'] = timedelta(minutes=0)
        for i in xrange(1,len(self.points)):
            point = self.points[i]
            speed = point['speed']
            lastPoint = self.points[i-1]
            distance = point['lastPointDistance']
            lastTime = lastPoint['calculateTotalTime']
            h = distance / speed
            ms = int((h * 3600) * 10**6)
            time = timedelta(microseconds=ms)
            point['calculatePointTime'] = time
            point['calculateTotalTime'] = lastTime + time
        
            #print 'Calculate = Total :' + str(totalTime) + ' time :'+ 
                            #str(time) + ' lastTime :' + str(lastTime + time)
                
def initFPL (adresse, points, routes, airport):
    """ Analysele fichier FDX """
    print 'Debut du traitement des FPL'
    log = ''
    lstFplFile = os.listdir(adresse)
    for file in lstFplFile :
        if 'FDX' in file :
            log += '=======================\n'
            log += 'File : ' + str(file) + '\n\n'
            lineClean = []
            line2 = ''
            lstFpl = []
            isFPL = False
            theLine = ''
            test = ''
            date = ''
            fplLine = []
            getLine = False
            fileAdresse = adresse + file
            fplFile = open(fileAdresse,'r') # Open the file   
            for line in fplFile.xreadlines(): # acts on each line of file
                line=line[0:-1]
                line = line.strip(None)
                if line :
                #removes comment lines and blank lines
                    fplLine.append(line)
            #print 'file ok'
            fplFile.close()
            
            for line in fplLine: # acts on each line of file
                if (r'(FPL-' in line[0:8] and r')' in line 
                                    and r'Text' not in line):
                    line2 = str(line)
                    getLine = True
                elif r'(FPL-' in line[0:8] and r'Text' not in line:
                    isFPL = True
                    theLine = ''
                    line2 = ''
                    theLine += str(line) + ' '
                elif isFPL == True and ETX in line:
                    isFPL = False
                    line2 = str(theLine)
                    getLine = True
                elif isFPL == True and r')' not in line:
                    theLine += str(line) + ' '
                elif isFPL == True:
                    isFPL = False
                    getLine = True
                    theLine += str(line) + ' '
                    line2 = str(theLine)
                # Find the date of the flight without DOF
                elif 'Updating RX event (for center AFTN) at  ' in line :
                    debut = line.find('at  ')
                    tabDate = line[debut+4:].split(' ')
                    #print tabDate
                    date = datetime(
                        int(tabDate[0]),
                        int(tabDate[1]),
                        int(tabDate[2]),
                        int(tabDate[3]),
                        int(tabDate[4]),
                        int(tabDate[5])
                        )
                    #print date
                        
                if getLine and line2 and line2 not in lineClean and date :
                    getLine = False
                    lineClean.append(line2)
                    theFpl = {
                        'line' : line2,
                        'date' : date
                        }
                    lstFpl.append(theFpl)            
            
            for theFpl in lstFpl :
                #print theFpl
                line = theFpl['line']
                date = theFpl['date']
                result = FPL.search(line)
                if result :
                    line = result.group(0)
                    fplObject = Fpl(line, date, points, routes, airport)
                else :
                    log += '  Bad line for :' + line + ' at ' + str(date) +'\n'

                #fplObject = Fpl(line, date, points, routes)
    allLog = log + '\n\n\n' + Fpl.log    
    writeLog('BadFpl',allLog)
    print 'Fin du traitement des FPL'
    return fpl
