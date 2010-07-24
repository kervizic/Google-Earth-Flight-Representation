#coding: utf-8
__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

import CharacteristicPoints, Routes, KML, Fdp, Aoi, Fpl, os, Ads
from usualFonction import *

cfg = open(r'manu.cfg','r') # Open the file 
section     = '' # correct value: "path" , "Style"
style       = {} # define the style dictionary
path        = {} # define the path dictionary
lookAt      = {} # define the LookAt dictionary
color       = {} # define the Color dictionary
comment     = {}
isOpen      = {}
makeFile    = {}
option      = {}
allObjects  = {}
lineClean   = []

def getOfConfigFile ():
    lineClean = cleanLine(cfg) # acts on each line of file

    for line in lineClean :
        if line[0:2] == "//" :
            section = ""
            if 'option' in line :
                section = 'option'
            elif 'path' in line :
                section = 'path'
            elif 'Style' in line :
                section = 'style'
            elif 'LookAt' in line :
                section = 'LookAt'
            elif 'Color' in line :
                section = 'Color'
            elif 'Comment' in line :
                section = 'Comment'
            elif 'open' in line :
                section = 'isOpen'
            elif 'update' in line :
                section = 'make'
        elif section == 'option' and line[0] != '/' :
            tmpLine = line.split('=')
            option[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))
        elif section == 'path' and line[0] != '/' :
            tmpLine = line.split('=')
            path[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))
        elif section == 'style' and line[0] != '/' :
            tmpLine = line.split('=')
            tmpSplit = tmpLine[1].split('-')
            name =str(tmpLine[0].strip(None))
            icon = tmpSplit[0].strip(None)
            scale = tmpSplit[1].strip(None)
            textColor = tmpSplit[2].strip(None)
            style[name] = {
                'icon' : icon,
                'scale' : scale,
                'color' : textColor
                }
        elif section == 'LookAt' and line[0] != '/' :
            tmpLine = line.split('=')
            lookAt[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))
        elif section == 'Color' and line[0] != '/' :
            tmpLine = line.split('=')
            color[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))
        elif section == 'Comment' and line[0] != '/' :
            tmpLine = line.split('=')
            comment[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))
        elif section == 'isOpen' and line[0] != '/' :
            tmpLine = line.split('=')
            isOpen[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))
        elif section == 'make' and line[0] != '/' :
            tmpLine = line.split('=')
            makeFile[str(tmpLine[0].strip(None))] = str(tmpLine[1].strip(None))

    allObjects ={
        'option' : option,
        'style' : style,
        'path': path,
        'lookAt' : lookAt,
        'color' : color,
        'comment' : comment,
        'makeFile' : makeFile,
        'isOpen' : isOpen
        }
    return allObjects


def getOfFile () :
    allObjects = getOfConfigFile ()    
    
    adresse = str(path['routesFilePath'])
    routes = Routes.initRT(adresse)
    
    adresse = path['characteristicsPointsFilePath']
    charactPoints, tahitiAirports = CharacteristicPoints.initCP(adresse)
    
    adresse = path['fdpFilePath']
    fdp = Fdp.initFDP(adresse)

    adresse = path['aoiFilePath']
    aoi = Aoi.initAOI(adresse)

    adresse = path['fplFilePath']
    fpl = Fpl.initFPL(adresse, charactPoints, routes['codedRoutes'])
    
    adresse = path['adsFilePath']
    ads = Ads.initADS(adresse, charactPoints, routes['codedRoutes'], fpl)

    allObjects['routes'] = routes
    allObjects['charactPoints'] = charactPoints
    allObjects['tahitiAirport'] = tahitiAirports
    allObjects['fdp'] = fdp
    allObjects['aoi'] = aoi
    allObjects['fpl'] = fpl
    allObjects['ads'] = ads
    return allObjects

