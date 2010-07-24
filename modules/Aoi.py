#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

print "Fir Charge =) "

import Convertion

from usualFonction import *

points     = {} 
aoi    = {}

class Points (object):
    """"All Points for the volume"""
        
    def __init__(self, donnees):
        """
        # Creat a new point
        #
        # definition of variables :
        #
        # self.name = str        is the name of route
        # self.coordinate = {}        is the coordinate of point
         """
        self.definition(donnees)
        # Add a route at the dictionary
        points[str(self.name)] = self

    def definition (self, donnees) :
        """ 
        # The data arrives in this form:
        # /Point/ 
        #
        #  NAME 
        #   |   COORDINATE
        #   |     |    
        # --V--|--V--
        #
        # The separation will therefore be using the separator "|"
        """
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        
        # Assigning variables
        self.name = str(tabDonnees[0])
        self.coordinate = Convertion.convertCoordinate(str(tabDonnees[1]))

class Aoi (object):
    lastAoi = '' # name of the last sid that has been entered
    
    def __init__(self, donnees, points):
        """
        # Creation of a new Volume
        #
        # definition of variables :
        #
        # self.name = str        is the name of route
        # self.altitude = {}
        # self.points = {}         is the list of points of the volume
        """
        self.defPoints = points
        self.points = {}
        self.altitude = {}
        self.definition(donnees)
        # Add a route at the dictionary
        aoi[str(self.name)] = self
        Aoi.lastAoi = str(self.name)
        
    def definition (self, donnees) :
        """ Disperssion des données 
        # The data arrives in this form:
        # /SID/ 
        # Convention is as follows:
        # 1st & 2nd character for the SID point
        # 3rd & 4th character for the SID number
        # 5th & 6th character for runway number: 5L=05L, 5R=05R, 
        #                                            3L=23L, 3R=23R
        #  NAME 
        #   |      COUCHE
        #   |        |        POINTS
        #   |        |          |   
        #   V        V          V       
        # ------|---------|----------------------
        #
        # La dispertion va donc de faire à l'aide du séparateur "|"
        """
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        # Assignation des variables    
        self.name = str(tabDonnees[0])
        tabLevel = tabDonnees[1].split('-')
        altMin = Convertion.convertLevel(str(tabLevel[0][1:].strip(None)))
        altMax = Convertion.convertLevel(str(tabLevel[1][1:].strip(None)))
        #print altMin
        #print altMax
        
        self.altitude['min'] = altMin
        self.altitude['max'] = altMax
        i = len(self.points)
        tabPoints = tabDonnees[2].split(' ')
        for x in tabPoints:
            if x != '' :
                self.points[i] = self.defPoints[x]
                i += 1
    
    def addPoints (self, donnees) :
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        # Assignation des variables    
        tabPoints = tabDonnees[2].split(' ')
        i = len(self.points)
        for x in tabPoints:
            if x != '' :
                self.points[i] = self.defPoints[x]
                i += 1
            

def initAOI (adresse):
    """ Analysele fichier FDP_VOLUMES_DEFINITION.ASF """
    
    fdp = open(adresse,'r') # Open the file 
    section = ""     # correct value: "points" or "aoi" 
                    # Used to be in the document.
    lineClean = cleanLine(fdp)
        
    #for line in fdp.xreadlines(): # acts on each line of file
        #if line[0] != "-" and len(line) > 5 :
        ##removes comment lines and blank lines
            #line=line[0:-1]
            #lineClean.append(line)
    
    for line in lineClean :
        if line[0] == "/" :
            section = ""
            if 'POINTS' in line :
                section = "points"
            elif 'SECTOR_AOI' in line :
                section = "aoi"

        if section == 'points' and line[0] != "/" :
            pt = Points(line)
        elif section == "aoi" and line[0] != "/" :
            if line[0] != '|' :
                a = Aoi(line, points)
            else :
                aoi[str(Aoi.lastAoi)].addPoints(line)


    allObjectsAoi = {
        'points'     : points,
        'aoi'        : aoi}
    return allObjectsAoi

