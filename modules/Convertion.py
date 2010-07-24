#coding: utf-8
__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""
import re  

COORDINATE = re.compile("""\
([0-9]{2})([0-9]{2})?([0-9]{2})?([NS])([0-9]{3})([0-9]{2})?([0-9]{2})?([EW])\
""")

def convertCoordinate (coordinate):
    """ Convert coordinates to decimal format 
    # This function saves the latitude and longitude of a point
    # In this system the North and East coordinates are positive
    # The South and West coordinates are negatives
    # hh:mm:ss d (hhmmd) => HH+MM/60+SS/3600*(D)
    """
    result = COORDINATE.search(coordinate)
    latH = result.group(1)
    latM = result.group(2)
    latS = result.group(3)
    latL = result.group(4)
    longH = result.group(5)
    longM = result.group(6)
    longS = result.group(7)
    longL = result.group(8)
    
    if latL == "N" :
        latD = float(1)
    elif latL == "S" :
        latD = float(-1)   
    else :
        latD = None
    if longL == "E" :
        longD = float(1)
    elif longL == "W" :
        longD = float(-1)   
    else :
        longD = None
    latitude = float(latH) * latD
    longitude = float(longH) * longD
    try :     
        latitude += float(latM)/60 * latD
        longitude += float(longM)/60 * longD
    except : 
        pass
    try :     
        latitude += float(latS)/3600 * latD
        longitude += float(longS)/3600 * longD
    except : 
        pass

    return {'latitude' : latitude, 'longitude' : longitude}


def convertLevel (level) :
    """
    This function converts a flight level in meters...
    """
    newLevel = float(level) * 30.479513
    return newLevel

import math


def distanceBetwennTwoPoint(lat1, long1, lat2, long2, altitude = 0):

    rayon = 6356.7523142 #km
    # Add the flight altitude
    rayon += (float(altitude)/1000) 
    # Convert to milles
    rayon = ( rayon / 1.852 ) 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = latitude
    phi1 = (lat1)*degrees_to_radians
    phi2 = (lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = ((math.sin(phi1)*math.sin(phi2) + 
           math.cos(phi1)*math.cos(phi2)*math.cos(theta1 - theta2) ))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in milles
    #print str(arc) + '*' + str(rayon)
    distance = float(arc) * float(rayon)
    return distance

def speedAndLevel(string) :
    """
    Cruising Speed or Mach Number
    The True Airspeed for the first or the whole cruising portion of
    the flight, in terms of:
        - K followed by 4 NUMERICS giving the True Airspeed in kilometres
        per hour, or
        - N followed by 4 NUMERICS giving the True Airspeed in knots, or
        - when so prescribed by the appropriate ATS authority, M followed by 3
        NUMERICS giving the Mach Number to the nearest hundredth of unit Mach.
    Requested Cruising Level
        - F followed by 3 NUMERICS, or
        - S followed by 4 NUMERICS, or
        - A followed by 3 NUMERICS, or
        - M followed by 4 NUMERICS, or
    See data conventions in 1.6 of page 283 of 4444 :
    - “F” followed by 3 decimal numerics: indicates a Flight Level Number,
    i.e. Flight Level 330 is expressed as “F330”;
    - “S” followed by 4 decimal numerics: indicates Standard Metric Level
    in tens of metres, i.e. Standard Metric Level 11 300 metres
    (Flight Level 370) is expressed as “S1130”;
    - “A” followed by 3 decimal numerics: indicates altitude in hundreds
    of feet, i.e. an altitude of 4 500 feet is expressed as “A045”;
    - “M” followed by 4 decimal numerics: indicates altitude in tens of
    metres, i.e. an altitude of 8 400 metres is expressed as “M0840”.
    """
    # Covert the speed in knots
    speed = ''
    altitude = ''
    if string[0] == 'K' :
        roughSpeed = int(string[1:5])
        level = string [5:]
        speed = (float(roughSpeed)/1.852)
    elif string[0] == 'N' :
        roughSpeed = int(string[1:5])
        level = string [5:]
        speed = roughSpeed
    elif string[0] == 'M' :
        roughSpeed = int(string[1:4])
        level = string [4:]
        speed = (float(roughSpeed)*6.6091283725993)
    else :
        print 'Convert Speed and Level error for : ' + str(string)
    if level[0] == 'F' :
        roughLevel = int(level[1:])
        altitude = convertLevel(roughLevel)
    elif level[0] == 'S' :
        roughLevel = int(level[1:])
        altitude = (float(roughLevel) * 10)
    elif level[0] == 'A' :
        roughLevel = int(level[1:])
        altitude = (float(roughLevel) * 0.3048 * 100)
    elif level == 'VFR' :
        #  Visual flight rules
        altitude = 0
    else :
        print 'Convert Speed and Level error for : ' + str(string)
    ret = {
        'speed' : speed,
        'altitude' : altitude
        }
    return ret

def testCoordinate() :

    coord = '803030N1201515W'

    for i in xrange(100000):
        coordi = convertCoordinate (coord)
    print coordi

if __name__ == '__main__' :
    import hotshot, os
    from time import gmtime, strftime
    print 'Execution du test : testCoordinate'
    profiler = hotshot.Profile("/home/manu/DTI/stats/statistiques.prf")
    profiler.runcall(testCoordinate)
    profiler.close()
    print 'Test OK, analise des donnees'
    time = strftime("%Y%m%d-%H%M%S", gmtime())
    name = ('convertCoordinate' + time +'.prof')
    cmd = """\
cd /home/manu/DTI/stats/
hotshot2calltree -o %s statistiques.prf
""" % name
    os.system(cmd)
    print 'Analyse OK'
    os.system('kcachegrind /home/manu/DTI/stats/%s' % name)

