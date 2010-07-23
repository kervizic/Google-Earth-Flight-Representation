
#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com)"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

print "ADS Charge =) "

import Convertion, os,re
from usualFonction import *
from time import gmtime, strftime
from datetime import datetime, timedelta

ads = {} 	# dictionary of Ads: { (x) : instance}
	
class Ads (object):

	
	def __init__(self, name, description, time, latitude, longitude):
		"""
		# Creation of a new route
		#
		# definition of variables :
		#
		# self.name = str		is the name of flight
		# list of points of the flight with type, time and coordinate
		# self.points = [{
		#	'type' : type,
		#   'time' : time,
		#	'latitude' : lat,
		#	'longitude' : long,	
		#	'altitude' : alt
		#	}] 
		 """
		self.points 		= {}
		self.tracks 		= {}
		self.name 			= name
		self.firstTime	= time
		self.nbPoints = 0
		self.nbTracks = 0
		self.addPoints ('Logon', description, time, latitude, longitude)
		ads[str(self.name)] = self
		

	def addPoints (self, type, description, time, latitude, longitude, altitude = 0) :
		"""
		Add points
		"""
		self.points[self.nbPoints] = {
			'type' : type,
			'time' : time,
			'latitude' : float(latitude),
			'longitude' : float(longitude),	
			'altitude' : altitude,
			'description' : description
			}
		self.nbPoints += 1
	
	def addTracks (self, type, description, time, latitude, longitude, altitude = 0) :
		"""
		Add Track : Point calculated by the TIARE systeme
		"""
		self.tracks[self.nbTracks] = {
			'type' : type,
			'time' : time,
			'latitude' : latitude,
			'latitude' : float(latitude),
			'longitude' : float(longitude),	
			'description' : description
			}
		self.nbTracks += 1
		
	def addPeriodic (self, description, time, latitude, longitude, altitude) :
		"""
		Add PERIODIC REPORT
		"""
		self.addPoints('Periodic Report', description, time, latitude, longitude, altitude)
	
	def addAltitudeEvent (self, description, time, latitude, longitude, altitude) :
		"""
		Add ALTITUDE RANGE DEVIATION EVENT 
		"""
		self.addPoints('Altitude Deviation', description, time, latitude, longitude, altitude)

	def addWaypointEvent (self, description, time, latitude, longitude, altitude) :
		"""
		Add WAYPOINT CHANGE EVENT
		"""
		self.addPoints('Waypoint Change', description, time, latitude, longitude, altitude)
		
def initADS (adresse, points, routes, fpl):
	#""" Analysele fichier ADS """
	lstAdsFile = os.listdir(adresse)
	dateRe = re.compile('(2[0-9]{3})([0-9]{2})([0-9]{2})')
	for file in lstAdsFile :
		if 'ADS' in file :
			fileAdresse = adresse + file
			adsFile = open(fileAdresse,'r') # Open the file   
			adsLine = adsFile.xreadlines()
			result = dateRe.search(file)
			date = datetime (
				year = int(result.group(1)),
				month = int(result.group(2)),
				day = int(result.group(3))
				)
			#print file
			#print date
			#print 'ADS file ok'
			buildAds(adsLine, date)
	#for key in ads :
		#print ads[key].name
		#for k in ads[key].points:
			#print '-- Point: ' +  str(ads[key].points[k]['type'])
			#for line in ads[key].points[k]['description']:
				#print '---- ' + str(line) 
	
	return ads

def buildAds (adsLine, date) :
	
	raz = True
	
	logonRe = re.compile(
		'([0-9]{2}):([0-9]{2}):([0-9]{2}) LOGON RECEIVED from (.+)'
		)
	logonCoordinateRe = re.compile(
		'Aircraft indicates position ([NS])([0-9]+)([EW])([0-9]+)'
		)
	periodicRe = re.compile(
		'PERIODIC REPORT REPORT RECEIVED for aircraft (.+) time stamped at : ([0-9]{2}):([0-9]{2}):([0-9]{2})'
		)
	waypointRe = re.compile(
		'WAYPOINT CHANGE EVENT REPORT RECEIVED for aircraft (.+) time stamped at : ([0-9]{2}):([0-9]{2}):([0-9]{2})'
		)
	altitudeRe = re.compile(
		'ALTITUDE RANGE DEVIATION EVENT REPORT RECEIVED for aircraft (.+) time stamped at : ([0-9]{2}):([0-9]{2}):([0-9]{2})'
		)
	coordinateRe = re.compile(
		'Basic Group  Lat :(.+) Long :(.+) Alt :(.+)'
		)
	trackRe =  re.compile(
		'start extrapolation for (.+) at: ([0-9]{2}):([0-9]{2}):([0-9]{2})'
		)
	trackLatLongRe =  re.compile(
		'Position Lat : ?(.+) Long: ?(.+)'
		)
	trackAltRe =  re.compile(
		'Altitude : ?(.+)'
		)
	reportRe = re.compile(
		'Report is correct'
		)
	endTrackRe = re.compile(
		'TRACK extrapolation completed'
		)
	
	i = 0
	l = 0	
	for line in adsLine :
		l +=1
		#print 'Line : ' + str(l)
		i -= 1
		# reset in case of errors
		if i == 0 or raz :
			if not raz :
				print 'error in ads file in line : ' + str(l)
			logon = ''
			periodic = ''
			waypointEvent = ''
			altitudeEvent = ''
			track = ''
			longitude = ''
			latitude = ''
			altitude = ''
			description = []
			time = False
			raz = False
			i = 0

		# Logon
		resultat = logonRe.search(line)
		if resultat :
			i = 5
			logon = resultat.group(4)
			time = datetime(
				date.year,
				date.month,
				date.day,
				int(resultat.group(1)),
				int(resultat.group(2)),
				int(resultat.group(3))
				)
		resultat = logonCoordinateRe.search(line)
		if resultat :
			lat = resultat.group(2)
			lon = resultat.group(4)
			latitude = (
				float(lat[0:2]) +  
				float(lat[2:4] + '.' + lon[4:])/60 
				)
			longitude = (
				float(lon[0:3]) +  
				float(lon[3:5] + '.' + lon[5:])/60
				)
			if resultat.group(1) == 'S':
				latitude = latitude * -1
			if resultat.group(3) == 'W':
				longitude = -1 * longitude
		# PERIODIC REPORT
		result = periodicRe.search(line)
		if result :
			i = 25
			periodic = result.group(1)
			time = datetime(
				date.year,
				date.month,
				date.day,
				int(result.group(2)),
				int(result.group(3)),
				int(result.group(4))
				)
		# ALTITUDE RANGE DEVIATION EVENT 
		result = altitudeRe.search(line)
		if result :
			i = 5
			altitudeEvent = result.group(1)
			time = datetime(
				date.year,
				date.month,
				date.day,
				int(result.group(2)),
				int(result.group(3)),
				int(result.group(4))
				)
		# WAYPOINT CHANGE EVENT
		result = waypointRe.search(line)
		if result :
			i = 10
			waypointEvent = result.group(1)
			time = datetime(
				date.year,
				date.month,
				date.day,
				int(result.group(2)),
				int(result.group(3)),
				int(result.group(4))
				)
		# AIRCRAFT INTENT TRACK: origin is EXTRAPOLATION
		result = trackRe.search(line)
		if result :
			i = 80
			track = result.group(1)
			time = datetime(
				date.year,
				date.month,
				date.day,
				int(result.group(2)),
				int(result.group(3)),
				int(result.group(4))
				)
		# AIRCRAFT INTENT TRACK Coordinate
		if track :
			result = trackLatLongRe.search(line)
			if result :
				latitude = result.group(1)
				longitude = result.group(2)
			result = trackAltRe.search(line)
			if result :
				altitude = result.group(1)
		# Coordinate
		result = coordinateRe.search(line)
		if result :
			latitude = result.group(1)
			longitude = result.group(2)
			altitude = result.group(3) 
		
		# Add the file lines in description argument
		if logon or periodic or waypointEvent or altitudeEvent or track:
			description.append(line)
		else :
			description = []
		
		# traitement des resultats
		
		# creating a new object has the appearance of a logon.
		if logon and longitude and latitude :
			#print 'Logon : ' + str(logon) + ' at ' + str(time) + ' Lat : ' + str(latitude) + ' - Long : ' + str(longitude)
			adsObject = Ads(logon, description, time, latitude, longitude)
			# reset attributes
			raz = True
		
		# Adding point at the onset of an event, periodic or not.
		result = reportRe.search(line)
		if result :
			if periodic :
				#print '\tPeriodic : ' + str(periodic) + ' at ' + str(time) + ' Lat : ' + str(latitude) + ' - Long : ' + str(longitude)
				ads[periodic].addPeriodic(description, time, latitude, longitude, altitude)
			elif waypointEvent :
				#print '\tWaypoint : ' + str(waypointEvent) + ' at ' + str(time) + ' Lat : ' + str(latitude) + ' - Long : ' + str(longitude)
				ads[waypointEvent].addWaypointEvent(description ,time, latitude, longitude, altitude)
			elif altitudeEvent :
				#print '\tAltitude : ' + str(altitudeEvent) + ' at ' + str(time) + ' Lat : ' + str(latitude) + ' - Long : ' + str(longitude)
				ads[altitudeEvent].addAltitudeEvent(description, time, latitude, longitude, altitude)
			# reset attributes
			raz = True
		
		# Adding track.
		result = endTrackRe.search(line)
		if result and track:
			ads[track].addTracks('TRACK', description, time, latitude, longitude, altitude)

			# reset attributes
			raz = True
	#fplFile.close()
	
	#return fpl
