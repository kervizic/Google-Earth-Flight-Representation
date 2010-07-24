from math import *
from decimal import *
from Convertion import *

AROUND = 10e15

def cleanLine (txtFile):
    lineClean = []
    for line in txtFile.xreadlines(): # acts on each line of file
        line=line[0:-1]
        line = line.strip(None)
        if line and line[0] != "#" and line[0] != '-':
        #removes comment lines and blank lines
            lineClean.append(line)
            #print '.' + str(line) + '.'
    return lineClean

def cleanLineWithComment (txtFile):
    lineClean = []
    for line in txtFile.xreadlines(): # acts on each line of file
        line=line[0:-1]
        line = line.strip(None)
        if line :
        #removes comment lines and blank lines
            lineClean.append(line)
            #print '.' + str(line) + '.'
    return lineClean

def round (num) :
    num = int(num*AROUND)
    return float(num/AROUND)
    
def sphericalToCartesian (lat,long):
    # converts spherical coordinates to cartesian coordinates in a point
    lat = radians(float(lat)) # converts degrees to radians 
    long = radians(float(long))
    x = cos(lat) * cos(long)
    y = cos(lat) * sin(long)
    z = sin(lat)
    coordinate = {
        'x' : x,
        'y' : y,
        'z' : z
        }
    return coordinate

def findPlane (lat1,long1,lat2,long2):
    #calculate the Cartesian coordinates (x, y, z) points 1 and 2 
    #using their spherical coordinates
    c1 = sphericalToCartesian(lat1,long1)
    c2 = sphericalToCartesian(lat2,long2)
    # the point 0 is the center of the earth
    # the plane through 0, c1 and c2 then the equation ax + by + cz = 0
    # a = y1 * z2 - z1 * y2
    # b = z1 * x2 - x1 * z2
    # c = x1 * y2 - y1 * x2 
    a = c1['y'] * c2['z'] - c1['z'] * c2['y'] 
    b = c1['z'] * c2['x'] - c1['x'] * c2['z'] 
    c = c1['x'] * c2['y'] - c1['y'] * c2['x'] 
    plane = {
        'a' : a,
        'b' : b,
        'c' : c
        }
    return plane
    
def verifyIntersection (line, point):
    positive = 360
    lat = float(point['latitude']) + positive
    long = float(point['longitude']) + positive
    lat1 = float(line['lat1']) + positive
    lat2 = float(line['lat2']) + positive
    long1 = float(line['long1']) + positive
    long2 = float(line['long2']) + positive
    tolerance = 0.01
    if lat1 > lat2 :
        maxLat = lat1 + tolerance
        minLat = lat2 - tolerance
    else :
        maxLat = lat2 +tolerance
        minLat = lat1 - tolerance
    if long1 > long2 :
        maxLong = long1 + tolerance
        minLong = long2 - tolerance
    else :
        maxLong = long2 + tolerance
        minLong = long1 - tolerance
    
    if minLat < lat < maxLat :
        if minLong < long < maxLong :
            return point

def findIntersection(line1 ,line2) :
    """
    line consists of two points defined by latitude and longitude :
    line = {
        'lat1' : lat1,
        'long1' : long1,
        'lat2' : lat2,
        'long2' : long2
        }
    in decimal
    """
    # find the plane of the line in cartesian coordianates
    p1 = findPlane(line1['lat1'],line1['long1'],
        line1['lat2'],line1['long2'],)
    p2 = findPlane(line2['lat1'],line2['long1'],
        line2['lat2'],line2['long2'],)
    # The intersection of two planes contains of course the 
    # point of origin, but also the point P : (x,y,z)
    # x = b1 * c2 - c1 * b2
    # y = c1 * a2 - a1 * c2
    # z = a1 * b2 - b1 * a2
    x = p1['b'] * p2['c'] - p1['c'] * p2['b'] 
    y = p1['c'] * p2['a'] - p1['a'] * p2['c'] 
    z = p1['a'] * p2['b'] - p1['b'] * p2['a'] 
    
    norme = sqrt(x**2+y**2+z**2)
    lat1 = degrees(asin(round(z/norme)))
    long1 = degrees(atan2(round(y),round(x)))
    lat2 = - (lat1)
    if long1 <= 0 :
        long2 = long1 + 180
    else :
        long2 = long1 - 180
    intersection1 = {'latitude' : lat1, 'longitude' : long1}
    intersection2 = {'latitude' : lat2, 'longitude' : long2}
    point = {'point1' : intersection1, 'point2' : intersection2}
    intersection = ''
    for key in point:
        p = point[key]
        i1 = verifyIntersection(line1,p)
        i2 = verifyIntersection(line2,p)
        if i1 == i2 and not intersection :
            intersection = i1    
    return intersection

def log(fileName, string, mode):
    date = strftime("%d%b%Y", gmtime())
    time = strftime("%a, %d %b %Y %H:%M:%S (DST Time): ", gmtime())
    file = open(filename + date + '.log', mode)
    file.write(string)
    file.close()
    
    
def testIntersection() : 
    for i in xrange(10000) :
        p11=convertCoordinate ('325111N0925021W')
        p12=convertCoordinate ('385942N0811837W')
        p21=convertCoordinate ('394023N0915033W')
        p22=convertCoordinate ('312426N0843429W')
        p=convertCoordinate ('353843N0880419W')
            
        line1 = {
            'lat1' : p11['latitude'],
            'long1' : p11['longitude'],
            'lat2' : p12['latitude'],
            'long2' : p12['longitude']
            }    
        line2 = {
            'lat1' : p21['latitude'],
            'long1' : p21['longitude'],
            'lat2' : p22['latitude'],
            'long2' : p22['longitude']
            }    
        #print 'point trouve :'
        intersection = findIntersection(line1 ,line2 )    
        #print 'point lu:'
        #print p
    
if __name__ == '__main__' :
    import hotshot, os
    from time import gmtime, strftime
    
    print 'Execution du test'
    profiler = hotshot.Profile("/home/manu/DTI/stats/statistiques.prf")
    profiler.runcall(testIntersection)
    profiler.close()
    print 'Test OK, analise des donnees'
    time = strftime("%Y%m%d-%H%M%S", gmtime())
    name = ('UsualFonction' + time +'.prof')
    cmd = """\
cd /home/manu/DTI/stats/
hotshot2calltree -o %s statistiques.prf
""" % name
    os.system(cmd)
    print 'Analyse OK'
    os.system('kcachegrind /home/manu/DTI/stats/%s' % name)
    

    
