#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

print "Fir Charge =) "

import Convertion
from usualFonction import *

points     = {} 
layers     = {}
volume     = {}
sector     = {}
fir     = {}

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
        # /CODED_ROUTE/ 
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

class Layer (object):
    """"All Points for the volume"""
    lastLevel ='0'
        
    def __init__(self, donnees):
        """
        # Creat a new Layer
        #
        # definition of variables :
        #
        # self.name = str        is the name of layer
        # self.level = {}        is the level of layer
         """
        self.definition(donnees)
        # Add a route at the dictionary
        layers[str(self.name)] = self

    def definition (self, donnees) :
        """ 
        # The data arrives in this form:
        # /CODED_ROUTE/ 
        #
        #  Couche (NAME) 
        #   |   Plafond
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
        newLevel = str(int(Convertion.convertLevel(float(tabDonnees[1][1:]))))
        self.level = {
            'min' : Layer.lastLevel,
            'max' : newLevel}
        Layer.lastLevel = newLevel
        
        
class Volume (object):
    lastVolume = '' # name of the last sid that has been entered
    
    def __init__(self, donnees, points, layers):
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
        self.layers = layers
        self.points = {}
        self.altitude = {}
        self.definition(donnees)
        # Add a route at the dictionary
        volume[str(self.name)] = self
        Volume.lastVolume = str(self.name)
        
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
        if '-' in tabDonnees[1] :
            tabLevel = tabDonnees[1].split('-')
            altMin = self.layers[str(tabLevel[0].strip(None))].level['min']
            altMax = self.layers[str(tabLevel[0].strip(None))].level['max']
            self.altitude['min'] = altMin
            self.altitude['max'] = altMax
        else :
            self.altitude = layers[str(tabDonnees[1])].level
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
            
class Sector (object):
    """all volume of NTTT Fire """
    lastSector = '' # name of the last sid that has been entered
    
    def __init__(self, donnees, volume, points, layers):
        """
        # Creation of a new Sector
        #
        # definition of variables :
        #
        # self.name = str        is the name of sector
        # self.volumes = {}     is the list of volumes of the sector
        """
        self.defVolume = volume
        self.volumes = {}
        self.definition(donnees)
        # Add a route at the dictionary
        sector[str(self.name)] = self
        Sector.lastSector = str(self.name)
        
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
        #   |      GCP 
        #   |        |       somme des volumes  
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
        tabVolumes = tabDonnees[2].split('+')
        for x in xrange(len(tabVolumes)) :
            tabVolumes[x] = tabVolumes[x].strip(None)
        i = len(self.volumes)
        for x in tabVolumes:
            if x != '' :
                self.volumes[i] = self.defVolume[x]
                i += 1
    
    def addVolume (self, donnees) :
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        # Assignation des variables    
        tabVolumes = tabDonnees[2].split('+')
        i = len(self.volumes)
        for x in xrange(len(tabVolumes)) :
            tabVolumes[x] = tabVolumes[x].strip(None)
        for x in tabVolumes:
            if x != '' :
                self.volumes[i] = self.defVolume[x]
                i += 1

class Fir (object):
    """all volume of NTTT Fire """
    lastFir = '' # name of the last sid that has been entered
    
    def __init__(self, donnees, volume, points, layers):
        """
        # Creation of a new Sector
        #
        # definition of variables :
        #
        # self.name = str        is the name of sector
        # self.volumes = {}     is the list of volumes of the sector
        """
        self.defVolume = volume
        self.volumes = {}
        self.definition(donnees)
        # Add a route at the dictionary
        fir[str(self.name)] = self
        Fir.lastFir = str(self.name)
        
    def definition (self, donnees) :
        """ Disperssion des données 
        # The data arrives in this form:
        # /FIR/
        #
        #  NAME 
        #   |          somme des volumes  
        #   |              |   
        #   V              V       
        # ------|--------------------------
        #
        # La dispertion va donc de faire à l'aide du séparateur "|"
        """
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        for x in xrange(len(tabDonnees)) :
            tabDonnees[x] = tabDonnees[x].strip(None)
        # Assignation des variables    
        self.name = str(tabDonnees[0])
        tabVolumes = tabDonnees[1].split('+')
        for x in xrange(len(tabVolumes)) :
            tabVolumes[x] = tabVolumes[x].strip(None)
        i = len(self.volumes)
        for x in tabVolumes:
            if x != '' :
                self.volumes[i] = self.defVolume[x]
                i += 1

def initFDP (adresse):
    """ Analysele fichier FDP_VOLUMES_DEFINITION.ASF """
    print 'Debut du traitement des FIR'
    fdp = open(adresse,'r') # Open the file 
    section = ""     # correct value: "coded route" , "sid" ou "star" 
                    #Used to be in the document.
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
            elif 'VOLUME' in line :
                section = "volume"
            elif 'LAYER' in line :
                section = "layer"
            elif 'SECTOR' in line :
                section = "sector"
            elif 'FIR' in line :
                section = "fir"

        if section == 'points' and line[0] != "/" :
            pt = Points(line)
        elif section == 'layer' and line[0] != "/" :
            lvl = Layer(line)
        elif section == "volume" and line[0] != "/" :
            if line[0] != '|' :
                vl = Volume(line, points, layers)
            else :
                volume[str(Volume.lastVolume)].addPoints(line)
        elif section == "sector" and line[0] != "/" :
            if line[0] != '|' :
                sec = Sector(line, volume, points, layers)
            else :
                sector[str(Sector.lastSector)].addVolume(line)
        elif section == "fir" and line[0] != "/" :
            if line[0] != '|' :
                sec = Fir(line, volume, points, layers)
            else :
                fir[str(Sector.lastSector)].addVolume(line)

    #for key in xrange(len(volume['G1'].points)) :
        #print str(volume['G1'].points[key].name)+ '   :' + str(volume['G1'].points[key].coordinate)
    #print 'test : ' + str(volume['G1'].points[0].coordinate)

    #for key in xrange(len(sector['VCC1'].volumes)) :
        #print str(sector['VCC1'].volumes[key].name)

    allObjectsFdp = {
        'points'     : points,
        'volume'     : volume,
        'layers'     : layers,
        'sector'     : sector,
        'fir'        : fir}
    print 'Fin du traitement des FIR'
    return allObjectsFdp

    
if __name__ == '__main__':
    adresse = '../Sources/FDP_VOLUMES_DEFINITION.ASF'
    test = initFDP(adresse)
