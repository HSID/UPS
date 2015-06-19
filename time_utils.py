#! /env/bin python

import re
import time
import calendar

def timeFormat(rawTimeString):
	"""
	rawTimeString: string- '2011-01-03-06:27:04.553' or '2014/05/21 04:10:58.593 PM'
	return: tuple-(string-'1213123123.232')
	"""
	weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	(year_str, month_str, day_str, hour_str, minute_str, sec_str, dSec_str) = re.findall(r'[0-9]+', rawTimeString)	
	weekday_str = weekdays[calendar.weekday(int(year_str), int(month_str), int(day_str))]
	month_str = months[int(month_str) - 1]
	timeString = '%s %s %s %s:%s:%s %s' % (weekday_str, month_str, day_str, hour_str, minute_str, sec_str, year_str)
	timeStructInLocal = time.strptime(timeString)
	timeSinceEpoch = (str(time.mktime(timeStructInLocal) + 12*60*60) if rawTimeString.find('PM') != -1 else str(time.mktime(timeStructInLocal)))
	return '.'.join([timeSinceEpoch.split('.')[0], dSec_str])




