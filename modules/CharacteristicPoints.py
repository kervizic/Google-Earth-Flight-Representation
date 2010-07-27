#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

import Convertion

print "CharcteristicPoints Charge =) "
characteristicPoints = {} # dictionaire de CharacteristicPoints : { (x) : instance}

class CharacteristicPoint :
    #number = 0 #numéro du points dans la liste
    
    def __init__(self, donnees):
        """
        # Création d'un point caractéristique 
        # Définition des variable :
        #
        # self.name = str
        # self.coordinate = str
        # self.latidtude = float
        # self.longitude = float        
        # self.theType = str        
        # self.comment = str        
        # self.airportListFixes = str        
        # self.relFix = bool    
        # self.pilDisplay = bool    
        # self.dti = bool
        """    

        self.addVariables(donnees)
        characteristicPoints[str(self.name)] = self # Ajout du point au dictionaire

    def addVariables (self, donnees) :
        """ Disperssion des données """
        # Les données arrivent sous la forme:
        # Name
        # |        Lat/Long
        # |           |       Type
        # |           |         |      Rel fix
        # |           |         |        |    Airport List fixes
        # |           |         |        |      |  PIL display
        # |           |         |        |      |       |  DTI
        # |           |         |        |      |       |   |  Comment
        # |           |         |        |      |       |   |    |
        # V           V         V        V      V       V   V    V
        # ------|-----------|-----------|---|---------|---|---|-------
        #
        # La dispertion va donc de faire à l'aide du séparateur "|"
        
        donnees = donnees.strip(None)
        tabDonnees = donnees.split("|")
        
        # Assignation des variables        
        self.name = tabDonnees[0].strip(None)
        self.coordinate = tabDonnees[1].strip(None)
        self.theType = tabDonnees[2].strip(None)
        self.airportListFixes = tabDonnees[4].strip(None)
        self.comment = tabDonnees[7].strip(None)
        if     tabDonnees[3].strip(None) == "Y" : 
            self.relFix = True
        else :
            self.relFix = False
        if     tabDonnees[5].strip(None) == "Y" : 
            self.pilDisplay = True
        else :
            self.pilDisplay = False
        if     tabDonnees[6].strip(None) == "Y" : 
            self.dti = True
        else :
            self.dti = False
        # Convertion des coordonnées en decimales
        self.decimalCoordinate = Convertion.convertCoordinate(self.coordinate)
        self.latitude = self.decimalCoordinate['latitude']
        self.longitude = self.decimalCoordinate['longitude']
        
        


def initCP (adresse):
    """ Creér le dictionnaire de Points characteritique
        à partir du fichier mentioné """
    print 'Debut du traitement des points characteistique'
    cp = open(adresse,'r') # Ouvre le fichier 
    for line in cp.xreadlines(): # agit sur chaque ligne du fichier
        #supprime lignes commentées et lignes vides
        if line[0] != "-" and line[0] != "/" and len(line) > 10 : 
            line=line[0:-1]
            cPoint = CharacteristicPoint(str(line))
    cp.close()
    # defines the airports owned by the Tahiti FIR
    tahitiAirports = []
    for key in characteristicPoints :
        cp = characteristicPoints[key]
        if cp.name[:2] == 'NT' and 'AIRPORT' in cp.theType:
            tahitiAirports.append(cp.name)
    print 'Fin du traitement des points characteistique'
    return characteristicPoints, tahitiAirports
