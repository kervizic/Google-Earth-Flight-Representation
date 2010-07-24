#coding: utf-8
__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

import CharacteristicPoints, Routes, KML, Fdp, GetOfFiles, usualFonction
import Convertion
from datetime import datetime, timedelta
from random import random

def addStyle (kml, allObjects) :
    for key in allObjects['style'] :
        theStyle = allObjects['style'][key]
        kml.addIconStyle(
            key, 
            theStyle['icon'], 
            theStyle['scale'], 
            theStyle['color'] 
            )
    #print 'Style OK !'
    return kml
    
def addCharctPoint (kml, point, visibility, style, lookAt) :
    position = lookAt.copy()
    position['longitude'] = point.longitude
    position['latitude'] = point.latitude
    description = [
        '<p>',
        'Type of the point : ' +  point.theType + '<br>',
        'Rel fix :' + str(point.relFix) + '<br>',
        'Airport List fixes : ' + str(point.airportListFixes) + '<br>',
        'PIL display : ' + str(point.pilDisplay) + '<br>',
        'DTI : ' + str(point.dti) + '<br>',
        'Comment : ' + str(point.comment) + '<br>',
        '</p>']
    kml.addPlacemark(
        point.name ,
        description ,
        position,
        visibility,
        style)
    return kml

def addVolume (kml, volume, color) :
    writeKml = kml.addMultiGeometry(
        volume.name,
        '',
        volume.points,
        volume.altitude,
        True,
        color)
    return kml
    
def addSurface(kml, volume, color) :
    writeKml = kml.addSurface(
        volume.name,
        '',
        volume.points,
        True,
        color)
    return kml
    
def addAllCharacteristicsPoints(allObjects):
    print "Start Characteristics points"
    kmlFileName = allObjects['comment']['CharacteristicsPointsFileName']
    kmlFileDescription = allObjects['comment']['CharacteristicsPointsFileDescription']
    lookAt = allObjects['lookAt']
    path = allObjects['path']['absCharacteristicsPointsPath']
    kml = KML.KML_File(
        path,
        kmlFileName,
        kmlFileDescription,
        allObjects['path']['kmlFilePath'],
        lookAt ,
        1)

    kml = addStyle(kml, allObjects)
    name = allObjects['comment']['AirPortFolderDescription']

    description = allObjects['comment']['AirportFolderName']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    cp = allObjects['charactPoints']
    for key in sorted(cp) :
        if 'AIRPORT' in cp[key].theType :
            style = 'airports'
            visibility = True
            kml = addCharctPoint(kml, cp[key], visibility, style, lookAt)
    #print "Aeroports ok"
    kml.close_folder()

    name = allObjects['comment']['DummyFolderName']
    description = allObjects['comment']['DummyFolderDescription']
    isOpen = 0
    kml.open_folder(name, description ,isOpen)
    cp = allObjects['charactPoints']
    for key in sorted(cp) :
        if 'DUMMY' in cp[key].theType :
            style = 'polygon'
            visibility = True
            kml = addCharctPoint(kml, cp[key], visibility, style, lookAt)
    #print "Dummy ok"
    kml.close_folder()

    name = allObjects['comment']['ReportFolderName']
    description = allObjects['comment']['ReportFolderDescription']
    isOpen = 0
    kml.open_folder(name, description ,isOpen)
    cp = allObjects['charactPoints']
    for key in sorted(cp) :
        if 'REPORT' in cp[key].theType :
            style = 'triangle'
            visibility = True
            kml = addCharctPoint(kml, cp[key], visibility, style, lookAt)
    #print "Report ok"
    kml.close_folder()

    name = allObjects['comment']['VorFolderName']
    description = allObjects['comment']['VorFolderDescription']
    isOpen = 0
    kml.open_folder(name, description , isOpen)
    cp = allObjects['charactPoints']
    for key in sorted(cp) :
        if 'VOR' in cp[key].theType :
            style = 'triangle'
            visibility = True
            kml = addCharctPoint(kml, cp[key], visibility, style, lookAt)
    #print "Vor ok"
    kml.close_folder()
    
    kml.close()
    print "Characteristics points file OK\n"
    return kml

def addRoutes(allObjects) :
    print "Start ROUTES"
    kmlFileName = allObjects['comment']['RoutesFileName']
    kmlFileDescription = allObjects['comment']['RoutesFileDescription']
    lookAt = allObjects['lookAt']
    path = allObjects['path']['absRoutesPath']
    kml = KML.KML_File(
        path,
        kmlFileName,
        kmlFileDescription,
        allObjects['path']['kmlFilePath'],
        lookAt ,
        1)

    kml = addStyle(kml, allObjects)

    name = allObjects['comment']['CodedRoutesFolderName']
    description = allObjects['comment']['CodedRoutesFolderDescription']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    cp = allObjects['routes']['codedRoutes']
    for key in sorted(cp) :
        color = '7F00FFFF'
        visibility = True
        width = 1
        name = cp[key].name
        description = ['sense : ' + str(cp[key].sense),]
        i=0
        points = {}
        for p in cp[key].points :
            points[i] = allObjects['charactPoints'][p].decimalCoordinate
            i += 1
        writeKml = kml.addLine (name ,description, color, points, visibility, width)
    #print "Coded line OK"
    kml.close_folder()
    
    name = allObjects['comment']['SidFolderName']
    description = allObjects['comment']['SidFolderDescription']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    cp = allObjects['routes']['sid']
    for key in sorted(cp) :
        color = '9F00FF00'
        visibility = True
        width = 1
        name = cp[key].name
        description = ['<b>airport: </b>' + str(cp[key].airport) + '<br>',
            '<b>Assigned RWY</b> : ' + str(cp[key].assigned)]
        i=0
        points = {}
        for p in cp[key].points :
            points[i] = allObjects['charactPoints'][p].decimalCoordinate
            i += 1
        writeKml = kml.addLine (name ,description, color, points, visibility, width)
    #print "SID OK"
    kml.close_folder()

    name = allObjects['comment']['StarFolderName']
    description = allObjects['comment']['StarFolderDescription']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    cp = allObjects['routes']['star']
    for key in sorted(cp) :
        color = '9F0000FF'
        visibility = True
        width = 1
        name = cp[key].name
        description = ['<b>airport: </b>' + str(cp[key].airport) + '<br>',
            '<b>Assigned RWY</b> : ' + str(cp[key].assigned)]
        i=0
        points = {}
        for p in cp[key].points :
            points[i] = allObjects['charactPoints'][p].decimalCoordinate
            i += 1
        writeKml = kml.addLine (name ,description, color, points, visibility, width)
    #print "STAR OK"
    kml.close_folder()

    kml.close()
    print "ROUTES file OK\n"
    return kml

def addSector (allObjects) :
    print "Start FIR"
    kmlFileName = allObjects['comment']['SectorFileName']
    kmlFileDescription = allObjects['comment']['SectorFileDescription']
    lookAt = allObjects['lookAt']
    path = allObjects['path']['absFirPath']
    kml = KML.KML_File(
        path,
        kmlFileName,
        kmlFileDescription,
        allObjects['path']['kmlFilePath'],
        lookAt ,
        1)

    kml = addStyle(kml, allObjects)

    # enable the deletion of the area during the approach
    if allObjects['option']['deleteZone'] == 'yes' :
        kml.addRegion()
    
    color = allObjects['color']

    name = allObjects['comment']['FirNTTTFolderName']
    description = allObjects['comment']['FirNTTTFolderDescription']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    sector = allObjects['fdp']['sector']
    for key in sorted(sector) :
        kml.open_folder(sector[key].name, '', False)
        for key2 in sorted(sector[key].volumes):
            volume = sector[key].volumes[key2]
            add = addSurface(kml, volume, color[sector[key].name])
        kml.close_folder()
    kml.close_folder()

    name = allObjects['comment']['AoiFolderName']
    description = allObjects['comment']['AoiFolderDescription']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    aoi = allObjects['aoi']['aoi']
    for key in sorted(aoi) :
        clr = color[aoi[key].name]
        description = allObjects['comment'][aoi[key].name]
        kml.open_folder(aoi[key].name, description, 0) # is not open
        add = addSurface(kml, aoi[key], clr)
        kml.close_folder()
    kml.close_folder()

    name = allObjects['comment']['FirExtFolderName']
    description = allObjects['comment']['FirExtFolderDescription']
    isOpen = 0
    kml.open_folder(name, description, isOpen)
    fir = allObjects['fdp']['fir']
    for key in sorted(fir) :
        clr = color[fir[key].name]
        kml.open_folder(fir[key].name, '', 0) # is not open
        for key2 in sorted(fir[key].volumes):
            volume = fir[key].volumes[key2]
            add = addSurface(kml, volume, clr)
        kml.close_folder()
    kml.close_folder()

    kml.close()
    print "FIR file OK\n"
    return kml

def addFpl(allObjects) :
    print "Start FPL"
    kmlFileName = allObjects['comment']['FplFileName']
    kmlFileDescription = allObjects['comment']['FplFileDescription']
    lookAt = allObjects['lookAt']
    path = allObjects['path']['absFplPath']
    kml = KML.KML_File(
        path,
        kmlFileName,
        kmlFileDescription,
        allObjects['path']['kmlFilePath'],
        lookAt ,
        1)

    kml = addStyle(kml, allObjects)
    
    fpl = allObjects['fpl']

    for key in sorted(fpl) :
        theFpl = fpl[key]
        name = theFpl.name
        description = fpl[key].description
        isOpen = 0
        kml.open_folder(name, description, isOpen)    
        deparatureTime = theFpl.deparatureTime
        estimatedTime = theFpl.estimatedTime
        arrivalTime = deparatureTime + estimatedTime
        color = '8F000000'
        visibility = True
        width = 1
        i=0
        points = {}
        description = [fpl[key].name,fpl[key].description]
        for p in theFpl.points :
            points[i] = fpl[key].points[p]['coordinate']
            i += 1
        begin = deparatureTime.strftime("%Y-%m-%dT%H:%MZ")
        end = arrivalTime.strftime("%Y-%m-%dT%H:%MZ")
        writeKml = kml.addLine (name ,description, color, points,
            visibility, width, begin, end)    
        x = random()
        x = x *16**6
        x = hex(int(x))
        tmpColor = 'FF' + str(x[2:].zfill(6))
        # add the flight in thge time
        for i in xrange(len(theFpl.points)-1) :
            tmpPoints = {}
            tmpPoints[0] = theFpl.points[i]['coordinate']
            tmpPoints[1] = theFpl.points[i+1]['coordinate']
            if tmpPoints[0] != tmpPoints[1] :
                tmpName = (
                    str(theFpl.points[i]['name']) + '-' +
                    str(theFpl.points[i+1]['name'])
                    )
                tmpBegin = (
                    deparatureTime + 
                    theFpl.points[i]['estimatedTotalTime']
                    )
                tmpEnd = (
                    deparatureTime + 
                    theFpl.points[i+1]['estimatedTotalTime']
                    )
                begin = tmpBegin.strftime("%Y-%m-%dT%H:%MZ")
                end = tmpEnd.strftime("%Y-%m-%dT%H:%MZ")
                tmpWidth = 4
                tmpDescription = [
                     str(tmpBegin.strftime("%H:%M")) + '-' +
                     str(tmpEnd.strftime("%H:%M")),
                     ]
                position = lookAt.copy()
                position['longitude'] = tmpPoints[0]['longitude']
                position['latitude'] = tmpPoints[0]['latitude']
                description =''
                style = 'avion'
                ptName = str(tmpBegin.strftime("%H:%M-")) + str(name)
                kml.addPlacemark(
                    ptName,
                    description ,
                    position,
                    visibility,
                    style,
                    begin,
                    end
                    )
                kml.addLine (
                    tmpName,
                    tmpDescription, 
                    tmpColor, 
                    tmpPoints,    
                    visibility, 
                    tmpWidth, 
                    begin, 
                    end
                    )
                # Find intrsection with AOI
                line1 = {
                    'lat1' : tmpPoints[0]['latitude'],
                    'long1' :  tmpPoints[0]['longitude'],
                    'lat2' : tmpPoints[1]['latitude'],
                    'long2' :  tmpPoints[1]['longitude'],
                    }
                aoi = allObjects['aoi']['aoi']
                for key in aoi :    
                    aoiPoints = aoi[key].points
                    for j in xrange(len(aoiPoints)-1) :
                        line2 = {
                            'lat1' : aoiPoints[j].coordinate['latitude'],
                            'long1' :  aoiPoints[j].coordinate['longitude'],
                            'lat2' : aoiPoints[j+1].coordinate['latitude'],
                            'long2' :  aoiPoints[j+1].coordinate['longitude'],
                            }
                        intersection = usualFonction.findIntersection(line1, line2)
                        if intersection:
                            distance = Convertion.distanceBetwennTwoPoint(
                                intersection['latitude'], 
                                intersection['longitude'], 
                                tmpPoints[0]['latitude'], 
                                tmpPoints[0]['longitude'], 
                                theFpl.points[i]['altitude']
                                )
                            pToPTime = theFpl.points[i+1]['estimatedPointTime']
                            pToPDistance =  theFpl.points[i+1]['lastPointDistance']
                            iTime = pToPTime *int(distance * 1000000000 / pToPDistance)
                            iTime =iTime  / 1000000000 
                            intersectionTime = tmpBegin + iTime
                            begin = deparatureTime.strftime("%Y-%m-%dT%H:%MZ")
                            end = arrivalTime.strftime("%Y-%m-%dT%H:%MZ")
                            position = lookAt.copy()
                            position['longitude'] = intersection['longitude']
                            position['latitude'] = intersection['latitude']
                            description =''
                            style = 'redCircle'
                            ptName = str(intersectionTime.strftime("%H:%M - ")) + str(name)
                            kml.addPlacemark(
                                ptName,
                                description ,
                                position,
                                visibility,
                                style,
                                begin,
                                end
                                )
        kml.close_folder()
    #print "FPL line OK"

    kml.close()
    print "FPL file OK\n"
    return kml

def addAds(allObjects) :
    print 'Start ADS'
    kmlFileName = allObjects['comment']['AdsFileName']
    kmlFileDescription = allObjects['comment']['AdsFileDescription']
    lookAt = allObjects['lookAt']
    path = allObjects['path']['absAdsPath']
    kml = KML.KML_File(
        path,
        kmlFileName,
        kmlFileDescription,
        allObjects['path']['kmlFilePath'],
        lookAt ,
        1)

    kml = addStyle(kml, allObjects)
    
    ads = allObjects['ads']

    for key in sorted(ads) :
        theAds = ads[key]
        points = theAds.points
        tracks = theAds.tracks
        name = theAds.name
        description = theAds.firstTime
        isOpen = 0
        kml.open_folder(name, description, isOpen)
        
        # Add TRACK
        kml.open_folder(
            'ADS', 
            'Point calculated by the TIARE systeme', 
            isOpen
            )
        deparatureTime = theAds.firstTime
        arrivalTime = points[len(points)-1]['time']
        color = '8F999999'
        visibility = True
        width = 1
        description=[]
        description.append(theAds.firstTime)
        begin = deparatureTime.strftime("%Y-%m-%dT%H:%MZ")
        end = arrivalTime.strftime("%Y-%m-%dT%H:%MZ")
        writeKml = kml.addLine (name ,description, color, points,
            visibility, width, begin, end)    
        x = random()
        x = x *16**6
        x = hex(int(x))
        tmpColor = 'FF' + str(x[2:].zfill(6))
        # add the flight in thge time
        if len(points) > 1 :
            for i in xrange(len(points)-1) :
                tmpPoints = {}
                tmpPoints[0] = point = points[i]
                tmpPoints[1] = nextPoint = points[i+1]
                
                tmpName = (
                    str(point['time'].strftime("H:%M")) + '-' +
                    str(nextPoint['time'].strftime("H:%M"))
                    )
                tmpBegin = (
                    point['time']
                    )
                tmpEnd = (
                    nextPoint['time']
                    )
                begin = tmpBegin.strftime("%Y-%m-%dT%H:%MZ")
                end = tmpEnd.strftime("%Y-%m-%dT%H:%MZ")
                tmpWidth = 4
                tmpDescription = [
                    str(name),
                    str(tmpBegin.strftime("%H:%M")) + '-' +
                    str(tmpEnd.strftime("%H:%M"))
                    ]
                position = lookAt.copy()
                position['longitude'] = point['longitude']
                position['latitude'] = point['latitude']
                description = []
                description.append('<p>')
                for line in point['description']:
                    description.append(line[:-1] + '<br>')
                description.append('</p>')
                style = 'avion2'
                ptName = str(theAds.name) + ' : ' + str(point['type']) + ' - ' + str(point['time'].strftime("%H:%M"))
                kml.addPlacemark(
                    ptName,
                    description ,
                    position,
                    visibility,
                    style,
                    begin,
                    end
                    )
                kml.addLine (
                    tmpName,
                    tmpDescription, 
                    tmpColor, 
                    tmpPoints,    
                    visibility, 
                    tmpWidth, 
                    begin, 
                    end
                    )
        point = points[len(points)-1]
        position = lookAt.copy()
        position['longitude'] = point['longitude']
        position['latitude'] = point['latitude']
        description = []
        description.append('<p>')
        for line in point['description']:
            description.append(line[:-1] + '<br>')
        description.append('</p>')
        style = 'avion2'
        ptName = str(point['type']) + ' - ' + str(point['time'].strftime("%H:%M"))
        kml.addPlacemark(
            ptName,
            description ,
            position,
            visibility,
            style,
            begin,
            end
            )
        kml.close_folder()
        # End Add ADS
        
        
        # Add TRACK
        kml.open_folder(
            'TRACK', 
            'Point calculated by the TIARE systeme', 
            isOpen
            )
        visibility = True
        for i in xrange(len(tracks)) :
            track = tracks[i]
            if i > 0 :
                lastTrack = tracks[i-1]
                tmpBegin = lastTrack['time']
            else :
                tmpBegin = track['time']
            begin = tmpBegin.strftime("%Y-%m-%dT%H:%MZ")                
            if i < len(tracks)-1:
                nextTrack = tracks[i+1]
                tmpEnd = nextTrack['time']
            else :
                tmpEnd = track['time']
            end = tmpEnd.strftime("%Y-%m-%dT%H:%MZ")
            position = lookAt.copy()
            position['longitude'] = track['longitude']
            position['latitude'] = track['latitude']
            description = []
            description.append('<p>')
            for line in track['description']:
                description.append(line[:-1] + '<br>')
            description.append('</p>')
            style = 'avion3'
            ptName = str(theAds.name) + ' : ' + str(track['type']) + ' - ' + str(track['time'].strftime("%H:%M"))
            kml.addPlacemark(
                ptName,
                description ,
                position,
                visibility,
                style,
                begin,
                end
                )
        
        kml.close_folder()
        # End Add TRACK
        kml.close_folder()
    

    kml.close()
    print "ADS file OK\n"
    return kml

def addMain (allObjects) :    
    print "Start MAin"
    kmlFileName = allObjects['comment']['MainFileName']
    kmlFileDescription = allObjects['comment']['MainFileDescription']
    lookAt = allObjects['lookAt']
    path= allObjects['path']['absMainPath']
    kml = KML.KML_File(
        path,
        kmlFileName,
        kmlFileDescription,
        allObjects['path']['kmlFilePath'],
        lookAt ,
        1)

    isOpen = 0
    lookAt = allObjects['lookAt']
    
    kml.addNetworkLink(
        allObjects['comment']['SectorFileName'],
        allObjects['comment']['SectorFileDescription'],
        isOpen,
        path = allObjects['path']['kmlFirPath'])
    kml.addNetworkLink(
        allObjects['comment']['RoutesFileName'],
        allObjects['comment']['RoutesFileDescription'],
        isOpen,
        path = allObjects['path']['kmlRoutesPath'])
    kml.addNetworkLink(
        allObjects['comment']['CharacteristicsPointsFileName'],
        allObjects['comment']['CharacteristicsPointsFileDescription'],
        isOpen,
        path = allObjects['path']['kmlCharacteristicsPointsPath'])
    kml.addNetworkLink(
        allObjects['comment']['FplFileName'],
        allObjects['comment']['FplFileDescription'],
        isOpen,
        path = allObjects['path']['kmlFplPath'])
    kml.addNetworkLink(
        allObjects['comment']['AdsFileName'],
        allObjects['comment']['AdsFileDescription'],
        isOpen,
        path = allObjects['path']['kmlAdsPath'])
    kml.close()
    print "Main file OK\n"

