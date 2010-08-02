#coding: utf-8
__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

import sys
sys.path.append(r'modules')
import CharacteristicPoints, Routes, KML, Fdp, GetOfFiles, MakeKML, Ads
import MakeKMZ, Aoi, os

def main():
    print ("""
######################################################################
## Representation des traces et routes des avions dans Google Earth ##
#    Programme realise par: KERVIZIC Emmanuel                        #
#      Pour :   La DTI de l'aviation civile                          #
##     Le :     17/06/2010                                          ##
######################################################################
\nC'est un bon debut ;)\n""")

    allObjects = GetOfFiles.getOfFile()
    makeFile = allObjects['makeFile']
    if makeFile['characteristicsPoints'] == 'yes':
        kmlCP = MakeKML.addAllCharacteristicsPoints(allObjects)
    if makeFile['routes'] == 'yes':
        kmlRT = MakeKML.addRoutes(allObjects)
    if makeFile['fir'] == 'yes':
        kmlST = MakeKML.addSector(allObjects)
    if makeFile['fpl'] == 'yes':
        kmlFP = MakeKML.addFpl(allObjects)
    if makeFile['ads'] == 'yes':
        kmlFP = MakeKML.addAds(allObjects)
    if makeFile['main'] == 'yes':
        kmlMain = MakeKML.addMain(allObjects)

    kmz = MakeKMZ.makeFile(allObjects)
    print "Et ca fini bien !"

# Execute only if this file is main
if __name__ == '__main__':
    main()
