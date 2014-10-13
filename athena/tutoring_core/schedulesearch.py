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
	"""
	Performs heavy lifting of core database queries
	"""

	# First, get all WeeklyTimeSlots that have a Tutor who has a Course which matches the query 
	timeslots = models.WeeklyTimeSlot.objects.filter(tutor__subjects__coursedept__iexact = course_dept, tutor__subjects__coursenum__iexact = course_num)

	# Then, filter out Tutors who do not have an ActiveTerm within the query
	timeslots = timeslots.filter(tutor__term__startdatetime__lte = date, tutor__term__enddatetime__gte = date)

	# TODO: filter out WeeklyTimeSlots that exists outside the bounds of the ActiveTerm

	return timeslots

def getScheduleJSON(date, course_dept, course_num):
	"""
	Gets a schedule from the database and nicely formats it in JSON for the frontend
	"""

	timeslots = getSchedule(date, course_dept, course_num)

	return timeslots