#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

print "Routes Charge =) "
from usualFonction import *
from time import gmtime, strftime
from datetime import datetime, timedelta

codedRoutes = {}     # dictionary of coded routes : { (x) : instance}
sid = {}            # dictionary of sid : { (x) : instance}
star = {}            # dictionary of star : { (x) : instance}
    
class CodedRoute (object):
    # name of the last route that has been entered
    lastRoute = "" 
    
    def __init__(self, donnees):
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
        self.definition(donnees)
        # Add a route at the dictionary
        codedRoutes[str(self.name)] = self
        CodedRoute.lastRoute = str(self.name)
        #time = strftime("%d%b%Y-%H:%M", gmtime())
        #file = open('LogRoutes' + time + '.log',"a")
        #file.write(self.log)
        #file.close()

    def definition (self, donnees) :
        """ 
        # The data arrives in this form:
        # /CODED_ROUTE/ 
        #
        #  NAME 
        #   |   SENSE  
        #   |     |   ODDS/EVENS or NONE
        #   |     |      |    
        #   |     |      |      
        #   |     |      |     LIST OF POINTS
        #   |     |      |           |
        # --V--|--V--|---V--|--------V--------|
        #
        # The separation will therefore be using the separator "|"
        """
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        
        # Assigning variables
        if len(tabDonnees) < 5 and len(tabDonnees) > 2 :
            self.name = str(tabDonnees[0])
            self.sense = str(tabDonnees[1])
            self.odds = str(tabDonnees[2])
            self.points = tabDonnees[3].split(" ")
        elif len(tabDonnees) > 5 :
            self.points.extend(tabDonnees[5].split(" "))
        self.log = self.name + ' :\n'
        for point in self.points :
            self.log += '\t' + point + ' :\n'
        
        
class Sid (object):
    lastSid = "" # name of the last sid that has been entered
    
    def __init__(self, donnees):
        """
        # Creation of a new sid
        #
        # definition of variables :
        #
        # self.name = str        is the name of route
        # self.airport = str
        # self.acft = str
        # self.assigned = str
        # self.points = []         is the list of points of the route
        # self.eligibleRoute = str 
        """
        
        self.definition(donnees)
        # Add a route at the dictionary
        sid[str(self.name)] = self
        Sid.lastSid = str(self.name)
        
    def definition (self, donnees) :
        """ Disperssion des données """
        # The data arrives in this form:
        # /SID/ 
        # Convention is as follows:
        # 1st & 2nd character for the SID point
        # 3rd & 4th character for the SID number
        # 5th & 6th character for runway number: 5L=05L, 5R=05R, 
        #                                            3L=23L, 3R=23R
        #  NAME 
        #   |      AIRPORT  
        #   |        |     ACFT PERFORMANCE CATEGORY
        #   |        |          |   ASSIGNED RWY
        #   |        |          |      |     LIST OF POINTS
        #   |        |          |      |       |
        #   V        V          V      V       V   
        # ------|---------|-------|-----|----------
        #
        # La dispertion va donc de faire à l'aide du séparateur "|"
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        
        # Assignation des variables    
        self.name = str(tabDonnees[0])
        self.airport = str(tabDonnees[1])
        self.acft = str(tabDonnees[2])
        self.assigned = str(tabDonnees[3])
        self.points = tabDonnees[4].split(" ")
    
    def setEligibleRoute (self, route) :
        tabRoute = route.split("|")
        route = tabRoute[1].strip(None)
        self.eligibleRoute = str(route)
    
        
class Star (object):
    # name of the last star that has been entered
    lastStar = "" 
    
    def __init__(self, donnees):
        """
        # Creation of a new sid
        #
        # definition of variables :
        #
        # self.name = str        is the name of route
        # self.airport = str
        # self.acft = str
        # self.atg = str
        # self.assigned = str
        # self.points = []         is the list of points of the route
        # self.eligibleRoute = str 
        """
        self.definition(donnees)
        # Add a route at the dictionary
        star[str(self.name)] = self
        Star.lastStar = str(self.name)
        
    def definition (self, donnees) :
        """ Disperssion des données """
        # The data arrives in this form:
        # /STAR/ 
        # Convention is as follows:
        # 1st & 2nd character for the SID point
        # 3rd & 4th character for the SID number
        # 5th & 6th character for runway number:
        #         5L=05L, 5R=05R, 3L=23L, 3R=23R
        #  NAME 
        #   |      AIRPORT  
        #   |       |    ACFT PERFORMANCE CATEGORY
        #   |       |         |     ATG ILS
        #   |       |         |       |   ASSIGNED RWY       
        #   |       |         |       |     |    LIST OF POINTS
        #   |       |         |       |     |      |
        #   V       V         V       V     V      V   
        # ------|---------|-------|-----|------|-------------
        #
        # La dispertion va donc de faire à l'aide du séparateur "|"
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        #print tabDonnees[0] + " " + tabDonnees[2] 
        
        # Assignation des variables    
        
        self.name = str(tabDonnees[0])
        self.airport = str(tabDonnees[1])
        self.acft = str(tabDonnees[2])
        self.atg = str(tabDonnees[3])
        self.assigned = str(tabDonnees[4])
        self.points = tabDonnees[5].split(" ")
    
    def setEligibleRoute (self, route) :
        tabRoute = route.split("|")
        route = tabRoute[1].strip(None)
        self.eligibleRoute = str(route)

    

def initRT (adresse):
    """ Analysele fichier ROUTE.ASF """
    
    cp = open(adresse,'r') # Open the file 
    section = ""     # correct value: "coded route" , "sid" ou "star" 
                    #Used to be in the document.
    lineClean = cleanLine(cp)
    
    #for line in cp.xreadlines(): # acts on each line of file
        #if line[0] != "-" and len(line) > 5 :
        ##removes comment lines and blank lines
            #line=line[0:-1]
            #lineClean.append(line)
    
    for line in lineClean :
        if line[0] == "/" :
            section = ""
            if line [1:12] == "CODED_ROUTE" :
                section = "coded route"
            elif line[1:4] == "SID" :
                section = "sid"
            elif line[1:5] == "STAR" :
                section = "star"

        if section == "coded route" and line[0] != "/" :
            if line[0] != "|" :
                crt = CodedRoute(line)
            else :
                codedRoutes[str(CodedRoute.lastRoute)].definition(line)
        elif section == "sid" and line[0] != "/" :
            if line[0:14] != "ELIGIBLE_ROUTE" :
                sd = Sid(line)
            else :
                sid[str(Sid.lastSid)].setEligibleRoute(line)
        elif section == "star" and line[0] != "/" :
            if line[0:14] != "ELIGIBLE_ROUTE" :
                sd = Star(line)
            else :
                star[str(Star.lastStar)].setEligibleRoute(line)
        
    cp.close()
    routes = {
        'codedRoutes' : codedRoutes,
        'sid' : sid,
        'star' : star }
    return routes
