__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com"
__version__ = "0.0.2"
__license__ = ""
__copyright__ =""

#__author__ = "Jon Goodall <jon.goodall@gmail.com> - http://www.duke.edu/~jgl34"
#__version__ = "0.0.1"

class KML_File (object):
    """ For creating KML files used for Google Earth """
    
    def __init__(self, filePath, name, description, kmlFilePath, lookAt, isOpen):
        """
        Inport array whith general longitude, latitude and all
        data necessary for a general LookAt.
        lookAt['altitude'] for all lookat
        lookAt['longitude'] for the folder longitude
        lookAt['llatitude'] for the folder latitude
        lookAt['tilt'] for all lookat
        lookAt['range'] for all lookAt
        lookAt['heading'] for all lookAt
        """
        self.filePath = filePath
        self.lookAt = lookAt
        self.kmlFilePath = kmlFilePath
        self.kml = ''
        self.name = name
        self.isOpen = str(isOpen) 
        self.ind = ''
        #adds the kml header to a file
        self.kml += """\
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name> %s </name>
<open> %s </open>
<description> %s </description>
<LookAt>
    <longitude> %s </longitude>
    <latitude> %s </latitude>
    <altitude> %s </altitude>
    <range> %s </range>
    <tilt> %s </tilt>
    <heading> %s </heading>
    <altitudeMode>absolute</altitudeMode>
    <gx:altitudeMode>absolute</gx:altitudeMode>
</LookAt>
""" % (
name, # String
self.isOpen, # String
description, # String
lookAt['longitude'], # String
lookAt['latitude'], # String
lookAt['altitude'], # String
lookAt['range'], # String
lookAt['tilt'], # String
lookAt['heading'] # String
)

    def addPlacemark(self, name ,description , position, visibility, 
    style = '', begin = '', end = ''):
        # adds the point to a kml file
        self.kml += """\
<Placemark>
<name> %s </name>
<visibility> %i </visibility>
<description><![CDATA[ %s ]]></description>
<styleUrl>#%s</styleUrl>
""" % (
name,
visibility,
description,
style,  # String
)
        if begin and end :
            self.kml += """\
<TimeSpan>
<begin> %s </begin>
<end> %s </end>
</TimeSpan>
""" % (
begin, # String
end # String
)
        self.kml += """\
<Point>
<altitudeMode>relativeToGround</altitudeMode>
<coordinates>%f,%f</coordinates>
</Point>
</Placemark>
""" % (
position['longitude'], # Float
position['latitude'] # Float
)

    def addLine (self, name ,description, color, points, visibility, 
    width, begin = '', end = '') :
        # adds the line to a kml file
        self.kml += """\
<Placemark>
<name> %s </name>
<visibility> %i </visibility>
<description><![CDATA[ %s ]]></description>
<Style>
<LineStyle>
<color> %s </color>
<width> %s </width>
</LineStyle>
</Style>
""" % (
name,
visibility,
description,
color,
width
)
        if begin and end :
            self.kml += """\
<TimeSpan>
<begin> %s </begin>
<end> %s </end>
</TimeSpan>
""" % (
begin, # String
end # String
)
        self.kml += """\
<LineString>
<tessellate>1</tessellate>
<coordinates>
"""
        for i in sorted(points) :
            self.kml += ('%f,%f\n') % (
                points[i]['longitude'], # Float
                points[i]['latitude'] # Float
                )
        self.kml += """\
</coordinates>
</LineString>
</Placemark>
"""

    def writeLookAt (self, lookAtTmp) :
        self.kml += """\
<LookAt>
<longitude> %s </longitude>
<latitude> %s </latitude>
<altitude> %s </altitude>
<range> %s </range>
<tilt>  %s </tilt>
<heading> %s </heading>
</LookAt>
""" % (
lookAtTmp['longitude'], # String
lookAtTmp['latitude'], # String
lookAtTmp['altitude'], # String
lookAtTmp['range'], # String
lookAtTmp['tilt'], # String
lookAtTmp['heading'] # String
)

    def addRegion (self) :
        self.kml += """\
<Region>
<LatLonAltBox>
<north>90</north>
<south>-90</south>
<east>180</east>
<west>-180</west>
<minAltitude>0</minAltitude>
<maxAltitude>-1</maxAltitude>
</LatLonAltBox>
<Lod>
<minLodPixels>-1</minLodPixels>
<maxLodPixels>200000</maxLodPixels>
<minFadeExtent>0</minFadeExtent>
<maxFadeExtent>200000</maxFadeExtent>
</Lod>
</Region>
"""

    def addTimeSpan (self, begin, end):
        self.kml += """\
<TimeSpan>
<begin> %s </begin>
<end> %s </end>
</TimeSpan>
""" % ( begin, end ) # String

    def open_folder(self, name, description, isOpen):
        self.kml += """\
<Folder>
<name> %s </name>
<description><![CDATA[ %s ]]></description>
<open> %s </open>
<LookAt>
<longitude> %s </longitude>
<latitude> %s </latitude>
<altitude> %s </altitude>
<range> %s </range>
<tilt>  %s </tilt>
<heading> %s </heading>
</LookAt>
""" % (
name, # String
description, # String
str(isOpen), # String
self.lookAt['longitude'], # String
self.lookAt['latitude'], # String
self.lookAt['altitude'], # String
self.lookAt['range'], # String
self.lookAt['tilt'], # String
self.lookAt['heading'] # String
)

    def close_folder(self):
        self.kml += '</Folder>\n'

    def openPlacemark (self, name, description, visibility):
        self.kml += """\
<Placemark>
<name> %s </name>
<visibility> %i </visibility>
<description><![CDATA[ %s ]]></description>
""" % (
name,
visibility,
description
)

    def addIconStyle (self, name, imgName, scale = '1', color = 'FFFFFFFF') :
        textScale = float(scale) + 0.3
        self.kml += """\
<Style id="%s">
<IconStyle>
<Icon>
<href>%simages/%s</href>
</Icon>
<scale> %s </scale>
</IconStyle>
<LabelStyle>
<color> %s </color>
<scale> %f </scale>
</LabelStyle>
</Style>
""" % (
name,
self.kmlFilePath,
imgName,
scale,
color,
textScale
)
            
    def addLineStyle (self, color, width) :
        self.kml += """\
<LineStyle>
<color> %s </color>
<width> %s </width>
</LineStyle>
""" % (
color, # String
width # String
)

    def addPolyStyle (self, color) :
        self.kml += """\
<PolyStyle>
<color> %s </color>
</PolyStyle>
""" % (color)  # String

    def addPolygon (self, polyPoints, altitudeMode):
        self.kml +="""\
<Polygon>
<altitudeMode> %s </altitudeMode>
<tessellate> %i </tessellate>
<outerBoundaryIs>
<LinearRing>
<coordinates>
""" % ( altitudeMode, 1 )
        for i in xrange(len(polyPoints)) :
            self.kml += '%s \n' % (polyPoints[i])  # String
        self.kml += """\
</coordinates>
</LinearRing>
</outerBoundaryIs>
</Polygon>
"""

    def addSurface (self, name, description, points, visibility, color) :
        # adds the line to a kml file
        self.kml += """\
<Placemark>
<name> %s </name>
<visibility> %i </visibility>
<description><![CDATA[ %s ]]></description>
<Style>
<LineStyle>
<color> %s </color>
<width> %s </width>
</LineStyle>
<PolyStyle>
<color> %s </color>
</PolyStyle>
</Style>
""" % (
name,
visibility,
description,
'FF' + str(color[2:]),
'0.5',
color
)
        self.kml +="""\
<Polygon>
<altitudeMode> %s </altitudeMode>
<tessellate> %i </tessellate>
<outerBoundaryIs>
<LinearRing>
<coordinates>
""" % ( 'clampToGround' , 1 )
        for i in xrange( len(points) - 1 ) :
            self.kml += ('%f,%f\n') % (
                points[i].coordinate['longitude'],
                points[i].coordinate['latitude']
                )
        self.kml += """\
</coordinates>
</LinearRing>
</outerBoundaryIs>
</Polygon>
</Placemark>
"""

    def addNetworkLink (self, name, description, isOpen, path,
                        refreshMode='onChange',refreshInterval=0 ):
        self.kml += """\
<NetworkLink>
<name> %s </name>
<description><![CDATA[ %s ]]></description>
<open> %s </open>
<LookAt>
<longitude> %s </longitude>
<latitude> %s </latitude>
<altitude> %s </altitude>
<range> %s </range>
<tilt>  %s </tilt>
<heading> %s </heading>
</LookAt>
<Url>
<href> %s </href>
<refreshMode> %s </refreshMode>
<refreshInterval> %s </refreshInterval>
</Url>
</NetworkLink>
""" % (
name, # String
description, # String
str(isOpen), # String
self.lookAt['longitude'], # String
self.lookAt['latitude'], # String
self.lookAt['altitude'], # String
self.lookAt['range'], # String
self.lookAt['tilt'], # String
self.lookAt['heading'], # String
path,  # String
refreshMode,  # String
refreshInterval # String
)

    def close(self):
        self.kml += '</Document>\n</kml>'
        print 'creation du fichier : ' + str(self.name)
        file = open(self.filePath,"w")
        with file :
            file.write(self.kml)
        print 'fichier: ' + str(self.name) +  ' est cree'

