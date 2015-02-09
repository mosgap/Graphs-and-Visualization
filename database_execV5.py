import MySQLdb
import time
import numpy
import math
import random
from sets import Set
import ast

ctr = 0;
current_time = 0;
print_table = numpy.array([[0,0,0,0]])

def __db():
	# declare query0,t as global
	global ctr,current_time,print_table
	#staticLoc = numpy.array([[1,37.1,91.1],[2,37.2,91.2],[3,37.3,91.3]])

	static_beacons = set([101,118,120,109,119,114,117,116,111,112,106,68,86,103,13,16])
	static_location = numpy.array([[101,9.98505,53.56225,1],[118,9.98537,53.56236,1],[120,9.98552,53.56239,1],[109,9.98548,53.56224,1],[119,9.98571,53.56222,1],[114,9.98548,53.56208,1],[117,9.98542,53.56197,1],[116,9.9855,53.56195,1],[111,9.9858,53.56181,2],[112,9.98496,53.5624,2],[106,9.98626,53.56166,2],[68,9.98534,53.56188,2],[86,9.98557,53.56196,2],[103,9.98536,53.5619,3],[13,9.986,53.56174,3],[16,9.98512,53.56229,3]])
	# connect to the database (host,username,password,database)
	db = MySQLdb.connect("188.166.49.200","nervous2","","nervous")
	fileLocation_f1 = 'mylocation1.txt'
	fileLocation_f2 = 'mylocation2.txt'
	fileLocation_f3 = 'mylocation3.txt'
	print "Connected to database...."
	#db = MySQLdb.connect("localhost","root","27feb1988","test1")

	# initialize cursors each for node,edge and other queries
	cn = db.cursor()
	ce = db.cursor()
	cc = db.cursor()
	indx = 0


	if ctr == 0:
		# initializing the first query
		query0 = "select MAX(RecordID) from SENSOR_b"
		cc.execute(query0)
		for x in cc:
			t = x;
		current_time = t[0]
		print current_time
		st = current_time


		# queries that finds the nodes and the edges
		query1 = 'select DISTINCT HEX(UUID),minor,rssi,Mac from SENSOR_b where RecordID <= %s AND minor IN (101,118,120,109,119,114,117,116,111,112,106,68,86,103,13,16)' % (current_time)
		query2 = 'select DISTINCT HEX(UUID),minor from SENSOR_b where RecordID <= %s AND minor IN (101,118,120,109,119,114,117,116,111,112,106,68,86,103,13,16)' % (current_time)

		cn.execute(query1);
		ce.execute(query2);

		temp_table = numpy.array([[0,0,0,0]])
		#uniq_table = []
		for x in cn.fetchall():
			pdist = float(x[2])/-59
			if pdist == 0:
				pdist = 0.6
			#uniq_table.append([x[0],x[1]])
			temp_table = numpy.append(temp_table,numpy.array([[x[0],x[1],pdist,x[3]]]),axis=0)
		temp_table = numpy.delete(temp_table,(0),axis=0)

		for x in ce.fetchall():
			goodvalues = [x[0],x[1]]
			ix = numpy.in1d(temp_table.ravel(),goodvalues).reshape(temp_table.shape)
			ind = numpy.unique(numpy.where(ix)[0])
			c2 = min(temp_table[ind,2])
			c3 = min(temp_table[ind,3])
			'''for y in ind:
				te = ast.literal_eval(temp_table[y,2])
				c2 = min(te,pdist,key=float)
				#print te
				if c2 == pdist:
					continue
				else:
					c3 = temp_table[y,3]
					pdist = te'''
			print_table = numpy.append(print_table,numpy.array([[x[0],x[1],c2,c3]]),axis=0)
					
					
		f1 = open(fileLocation_f1,'w')
		f2 = open(fileLocation_f2,'w')
		f3 = open(fileLocation_f3,'w')
		print>> f1,'['
		print>> f2,'['
		print>> f3,'['
		#seenU = numpy.array([[-1]])
		seenB = numpy.array([[-1]])
		locU1 = set()
		locU2 = set()
		locU3 = set()
		for x in print_table:
			#tempU = numpy.array([[x[0]]])
                        tempB = numpy.array([[x[1]]])

			if x[3] == 0:
				ptype  = 'iPhone'
			else:
				ptype = 'Android'

			'''seensetU = set([tuple(y) for y in seenU[:,:1]])
                        tempsetU = set([tuple(y) for y in tempU[:,:1]])
                        c = numpy.array([y for y in seensetU & tempsetU])'''
                        seensetB = set([tuple(y) for y in seenB[:,:1]])
                        tempsetB = set([tuple(y) for y in tempB[:,:1]])
                        d = numpy.array([y for y in seensetB & tempsetB])

			for i in range(0,len(static_location)):
				#a = len(numpy.intersect1d(numpy.array([[x[1]]]),static_location[i,0]))
				if ast.literal_eval(x[1]) != static_location[i,0]:
					continue
				else:
					doit = 1
					if static_location[i,3] == 1:
						f = f1
						if len(locU1.intersection(set([x[0]]))) != 0:
							doit = 0
					if static_location[i,3] == 2:
						f = f2
						if len(locU2.intersection(set([x[0]]))) != 0:
							doit = 0
					if static_location[i,3] == 3:
						f = f3
						if len(locU3.intersection(set([x[0]]))) != 0:
							doit = 0
					if doit == 1:
						#seenU = numpy.append(seenU,tempU,axis=0)
						if static_location[i,3] == 1:
							locU1.add(x[0])
						if static_location[i,3] == 2:
							locU2.add(x[0])
						if static_location[i,3] == 3:
							locU3.add(x[0])
                       				print>> f,'{"cn":{"%s":{"label":"Phone (%s)","size":10,"color":"0x00ff00","lat":%s,"lon":%s}}},' % (x[0],ptype,static_location[i,2]+(float(x[2])/100000),static_location[i,1]+(float(x[2])/100000))
					if d.size == 0:
						seenB = numpy.append(seenB,tempB,axis=0)
						
                       				print>> f,'{"cn":{"%s":{"label":"Beacon %s","size":10,"color":"0xff0000","lat":%s,"lon":%s}}},' % (x[1],x[1],static_location[i,2],static_location[i,1])
					print>> f,'{"ce":{"%s%s":{"source":"%s","target":"%s","weight":%s,"directed":false}}},' % (x[0],x[1],x[0],x[1],1)

		ctr = ctr + 1
		print '-----'

	else:
		# for the next iteration
		query0 = "select MAX(RecordID) from SENSOR_b"
		cc.execute(query0)
		for x in cc:
			t = x;
		print t[0]
		if t[0] <= current_time:
			return

		query1 = 'select DISTINCT HEX(UUID),minor,rssi,Mac from SENSOR_b where RecordID > %s AND RecordID <= %s AND minor IN (101,118,120,109,119,114,117,116,111,112,106,68,86,103,13,16)' % (current_time,t[0])
		query2 = 'select DISTINCT HEX(UUID),minor from SENSOR_b where RecordID > %s AND RecordID <= %s AND minor IN (101,118,120,109,119,114,117,116,111,112,106,68,86,103,13,16)' % (current_time,t[0])
		cn.execute(query1);
		ce.execute(query2);

		temp_table = numpy.array([[0,0,0,0]])
		#uniq_table = []
		for x in cn.fetchall():
			pdist = float(x[2])/-59
			if pdist == 0:
				pdist = 0.6
			#uniq_table.append([x[0],x[1]])
			temp_table = numpy.append(temp_table,numpy.array([[x[0],x[1],pdist,x[3]]]),axis=0)
		temp_table = numpy.delete(temp_table,(0),axis=0)

		for x in ce.fetchall():
			goodvalues = [x[0],x[1]]
			ix = numpy.in1d(temp_table.ravel(),goodvalues).reshape(temp_table.shape)
			ind = numpy.unique(numpy.where(ix)[0])
			c2 = min(temp_table[ind,2])
			c3 = min(temp_table[ind,3])
			print_table = numpy.append(print_table,numpy.array([[x[0],x[1],c2,c3]]),axis=0)
					
					
		f1 = open(fileLocation_f1,'w')
		f2 = open(fileLocation_f2,'w')
		f3 = open(fileLocation_f3,'w')
		print>> f1,'['
		print>> f2,'['
		print>> f3,'['
		#seenU = numpy.array([[-1]])
		seenB = numpy.array([[-1]])
		for x in print_table:
			#tempU = numpy.array([[x[0]]])
                        tempB = numpy.array([[x[1]]])

			if x[3] == 0:
				ptype  = 'iPhone'
			else:
				ptype = 'Android'

			'''seensetU = set([tuple(y) for y in seenU])
                        tempsetU = set([tuple(y) for y in tempU])
                        c = numpy.array([y for y in seensetU & tempsetU])'''
                        seensetB = set([tuple(y) for y in seenB])
                        tempsetB = set([tuple(y) for y in tempB])
                        d = numpy.array([y for y in seensetB & tempsetB])

			for i in range(0,len(static_location)):
				#a = len(numpy.intersect1d(numpy.array([[x[1]]]),static_location[i,0]))
				if ast.literal_eval(x[1]) != static_location[i,0]:
					continue
				else:
					doit = 1
					if static_location[i,3] == 1:
						f = f1
						if len(locU1.intersection(set([x[0]]))) != 0:
							doit = 0
					if static_location[i,3] == 2:
						f = f2
						if len(locU2.intersection(set([x[0]]))) != 0:
							doit = 0
					if static_location[i,3] == 3:
						f = f3
						if len(locU3.intersection(x[0])) != 0:
							doit = 0
					if doit == 1:#c.size == 0 or doit == 1:
						#seenU = numpy.append(seenU,tempU,axis=0)
						if static_location[i,3] == 1:
							locU1.add(x[0])
						if static_location[i,3] == 2:
							locU2.add(x[0])
						if static_location[i,3] == 3:
							locU3.add(x[0])
						#seenU = numpy.append(seenU,tempU,axis=0)
                       				print>> f,'{"cn":{"%s":{"label":"Phone (%s)","size":10,"color":"0x00ff00","lat":%s,"lon":%s}}},' % (x[0],ptype,static_location[i,2]+(float(x[2])/100000),static_location[i,1]+(float(x[2])/100000))
					if d.size == 0:
						seenB = numpy.append(seenB,tempB,axis=0)
                       				print>> f,'{"cn":{"%s":{"label":"Beacon %s","size":10,"color":"0xff0000","lat":%s,"lon":%s}}},' % (x[1],x[1],static_location[i,2],static_location[i,1])
					print>> f,'{"ce":{"%s%s":{"source":"%s","target":"%s","weight":%s,"directed":false}}},' % (x[0],x[1],x[0],x[1],1)

		current_time = t[0]



	print>> f1,']'
	print>> f2,']'
	print>> f3,']'

if __name__ == "__main__":
	while True:
		__db()
		time.sleep(100)
