#coding: utf-8
__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""


import sys
sys.path.append(r'modules')
import CharacteristicPoints, Routes, KML, Fdp, GetOfFiles, MakeKML, Ads
import MakeKMZ, Aoi, os


print "###################################################################### "
print "## Representation des traces et routes des avions dans Google Earth ## "
print "#  Programme realise par:                                            # "
print "#      KERVIZIC Emmanuel                                             # "
print "#  Pour :                                                            # "
print "#      La DTI de l'aviation civile                                   # "
print "#  Le :                                                              # "
print "##     17/06/2010                                                   ## "
print "###################################################################### "
print ""
print "C'est un bon debut ;) "
print ""

#adresse = r'/media/Manu/DTI/Sources/'
#adresse2 = r'/media/Manu/DTI/Sources/'
#lstFplFile = os.listdir(adresse)
#for file in lstFplFile :
	#if '.7z' in file :
		#print "7z e " + adresse2 + str(file)
		#os.system("7z e " + adresse + str(file)) 
	

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
#os.system("c:/windows/notepad.exe monfichier.log")
#print allObjects['fdp']['volume']
print "Et ca fini bien !"

