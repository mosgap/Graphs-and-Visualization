# The code plots the output time window size vs percentage missing values
# for the proximity data collected by the nervous net app.
# The code was written by Siddhartha for
#              ------------------------------------------------------
# 		           Computational Social Science
# 	       Department of Humanities, Social and Political Sciences
# 		          Prof. Dirk Helbing (ETH, Zurich)
#             			Clausiusstrasse 50
# 				   CLU Building
# 			     8092 Zürich, Switzerland
#              ------------------------------------------------------

import MySQLdb
import time
from numpy import *
import math
import datetime
from sets import Set
import matplotlib.pyplot as plt

def __getGranularity(window_size):
	# connect to the local SQL database where the data is.
	# connect to the database (host,username,password,database)
	db = MySQLdb.connect("localhost","root","27feb1988","CCC");
	print "Successful Connection....";

	# get the node cursor
	cn = db.cursor();

	# find the minimum and maximum timestamp
	query0 = 'select min(RecordTime) from SENSOR_b';
	cn.execute(query0);

	for x in cn.fetchall():
		min_timestamp = x[0];
	max_timestamp = 1420066799000;

	# find all unique UUIDs
	uuids = set();
	query0 = 'select DISTINCT HEX(UUID) from SENSOR_b WHERE RecordTime <= %s' % max_timestamp;
	cn.execute(query0);

	for x in cn.fetchall():
		uuids.add(x);
	sl = list(uuids);
	#print sl;
	

	# find the final window size and total #windows
	# total #windows is leaving out the final window if the
	# size of the database does not exactly match the selected
	# window size.
	final_windowsize = (max_timestamp-min_timestamp) % (window_size*1000);
	if final_windowsize > 0:
		e = 1;
	else:
		e = 0;
	total_window = (max_timestamp-min_timestamp-final_windowsize)/(window_size*1000);
	print '%s windows being processed' % total_window;

	# get the first initial time and the (final time of the first window +1)
	current_time = min_timestamp;
	end_time = current_time + window_size*1000;

	# initiaze the array of zeros to keep track of the number of
	# windows in which each uuid is missing.
	percent_missing = zeros((len(uuids),1));

	# start iterating the windows
	for i in range(0,total_window):
		uuids_cw = set();
		uuids_ncw = set();
		query0 = 'SELECT DISTINCT HEX(UUID) FROM  SENSOR_b WHERE RecordTime BETWEEN %s AND %s' % (current_time,(end_time-1));
		current_time = end_time;
		end_time = current_time + window_size*1000;

		cn.execute(query0);
		for x in cn.fetchall():
			uuids_cw.add(x);
		
		uuids_ncw = uuids.difference(uuids_cw);
		for x in uuids_ncw:
			indx = sl.index(x);
			percent_missing[indx,0] += 1;

	# do one final windowing if the database size exactly does not fit the window size.
	if e == 1:		
		uuids_cw = set();
	        uuids_ncw = set();
		end_time = current_time + final_windowsize;

	        query0 = 'SELECT DISTINCT HEX(UUID) FROM  SENSOR_b WHERE RecordTime BETWEEN %s AND %s' % (current_time,(end_time-1));

        	cn.execute(query0);
	        for x in cn.fetchall():
     			uuids_cw.add(x);

   		uuids_ncw = uuids.difference(uuids_cw);
    		for x in uuids_ncw:
        		indx = sl.index(x);
            		percent_missing[indx,0] += 1;


	return percent_missing/float(total_window+e),uuids

if __name__ == "__main__":
	percent_list = [];
	window_size = [];
	for win in range(600,30001,600):
		print '------------------------------------------------';
		print '          Window size %s seconds             ' % win;
		print '------------------------------------------------';
		percent_array, uuid = __getGranularity(win);
		temp_list = [x[0] for x in percent_array];
		percent_list.append(temp_list);
		window_size.append(win);
		print 'Finished successfully....';
	percent_list = array(percent_list);

	'''filename = 'percent_missing.txt';
	f = open(filename,'w');

	for x in window_size:
		print >> f,' %s ,' % x;
	for x in uuid:
		print >> f,' %s ,' % x;
	for i in range(0,len(percent_array)):
		for j in range(0,len(uuid)):
			print >> f,' %s,' % percent_array[i][j];'''

	for i in range(0,len(uuid)):
		plt.plot(window_size,list(percent_list[:,i]));
		plt.hold(True);

	plt.xlabel('WINDOW SIZE in seconds');
	plt.ylabel('PERCENTAGE MISSING');
	plt.title('GRANULARITY PLOT');
	plt.grid(True);
	plt.show();
