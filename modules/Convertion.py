#coding: utf-8
__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

def convertCoordinate (coordinate):
	""" Convert coordinates to decimal format """
	# 3 solution sont possible : 7, 11 ou 15 charactères
	if len(coordinate) == 7 : # heures seules
		latitude = addLatitude(str(coordinate[0:3]))
		longitude = addLongitude(str(coordinate[3:7]))
	elif len(coordinate) == 11 : # heures et minutes
		latitude = addLatitude(str(coordinate[0:5]))
		longitude = addLongitude(str(coordinate[5:11]))
	elif len(coordinate) == 15 : # heures, minutes et secondes
		latitude = addLatitude(str(coordinate[0:7]))
		longitude = addLongitude(str(coordinate[7:15]))
	coordinate = {'latitude' : latitude, 'longitude' : longitude}
	return coordinate

			
		
def addLatitude (latitude):
	""" This function saves the latitude of a point
	# In this system the North and East coordinates are positive
	# The South and West coordinates are negatives
	# hh:mm:ss d (hhmmd) => HH+MM/60+SS/3600*(D)
	 """
	latitudeD = ''
	if len(latitude) == 3 : # Si seulement heures
		h = float(latitude[0:2]) #Seletionne les deux premiers charactères
		if str(latitude[2]) == "N" : #Défini la polarité
			d = float(1)
		elif str(latitude[2]) == "S" :
			d = float(-1)				
		latitudeD = float( h * d ) #Convertion en décimale
	elif len(latitude) == 5 : # Si heures et minutes
		h = float(latitude[0:2])
		m = float(latitude[2:4])
		if str(latitude[4]) == "N" :
			d = float(1)
		elif str(latitude[4]) == "S" :
			d = float(-1)				
		latitudeD = float( ( h + m / 60 ) * d ) 
	elif len(latitude) == 7 : # Si heures et minutes
		h = float(latitude[0:2])
		m = float(latitude[2:4])
		s = float(latitude[4:6])
		if str(latitude[6]) == "N" :
			d = float(1)
		elif str(latitude[6]) == "S" :
			d = float(-1)				
		latitudeD = float( ( h + m / 60 + s / 3600) * d )
	return latitudeD

		
def addLongitude (longitude):
	""" This function saves the latitude of a point
	# In this system the North and East coordinates are positive
	# The South and West coordinates are negative
	# hh:mm:ss d (hhmmd) => HH+MM/60+SS/3600*(D)
	"""
	longitudeD =''
	if len(longitude) == 4 : # cf. Latitude
		h = float(longitude[0:3])
		if str(longitude[3]) == "E" :
			d = float(1)
		elif str(longitude[3]) == "W" :
			d = float(-1)				
		longitudeD = float( h * d )
	elif len(longitude) == 6 :
		h = float(longitude[0:3])
		m = float(longitude[3:5])
		if str(longitude[5]) == "E" :
			d = float(1)
		elif str(longitude[5]) == "W" :
			d = float(-1)				
		longitudeD = float( ( h + m / 60 ) * d )
	elif len(longitude) == 8 :
		h = float(longitude[0:3])
		m = float(longitude[3:5])
		s = float(longitude[5:7])
		if str(longitude[7]) == "E" :
			d = float(1)
		elif str(longitude[7]) == "W" :
			d = float(-1)				
		longitudeD = float( ( h + m / 60 + s / 3600) * d )
	return longitudeD

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


