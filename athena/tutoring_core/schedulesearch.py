from tutoring_core import models

import datetime as dt

def getWeekDays(date):
	"""
	Given a datetime.date, return a list of the other datetime.date objects in the
	same Monday-based week
	"""

	weekday = date.weekday()
	return [date + dt.timedelta(days = offset) for offset in range(0 - weekday, 7 - weekday)]

def getSchedule(date, course_dept, course_num):
	pass

def getScheduleJSON(date, course_dept, course_num):
	getSchedule(date, course_dept, course_num)

	return []