import math
import datetime

from xmpp_monitor import database
from dateutil.parser import parse as dateparse

def create_summary():
	startdate = dateparse('T00:00:00-04:00')
	enddate = dateparse('T00:00:00-04:00')
	status = {}
	total = datetime.timedelta()
	for event in database.get_events(startdate=startdate, enddate=enddate):
		if event['status'] not in status:
			status[event['status']] = datetime.timedelta()
		duration = event['end'] - event['start']
		status[event['status']] += duration
		total += duration


	for x in status:
		summary = {
			'date': datetime.datetime.today(),
			'status': x,
			'percentage': math.floor((status[x] / total) * 100)
		}
		print(summary)

	print('done')
	pass