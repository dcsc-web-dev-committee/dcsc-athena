from tutoring_core import models

import datetime as dt

def getWeekDays(date):
	"""
	Given a datetime.date, return a list of the other datetime.date objects in the
	same Monday-based week
	"""

	weekday = date.weekday()
	return [date + dt.timedelta(days = offset) for offset in range(0 - weekday, 7 - weekday)]

def getDayAsString(i):
	return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i]

def getSchedule(date, course_dept, course_num):
	"""
	Performs heavy lifting of core database queries
	"""

	weekdays = getWeekDays(date)

	# First, get all WeeklyTimeSlots that have a Tutor who has a Course which matches the query 
	timeslots = models.WeeklyTimeSlot.objects.filter(tutor__subjects__coursedept__iexact = course_dept, tutor__subjects__coursenum__iexact = course_num)

	# Then, filter out Tutors who do not have an ActiveTerm within the query
	timeslots = timeslots.filter(tutor__term__startdatetime__lte = date, tutor__term__enddatetime__gte = date)

	# TODO: filter out WeeklyTimeSlots that exists outside the bounds of the ActiveTerm
	# TODO: check for TimeOffs
	# TODO: add MakeUp hours
	# TODO: check for holidays

	schedule = {}

	for timeslot in timeslots:
		# Get day and time in question
		day = getDayAsString(timeslot.day)

		# Set reference to which day we are looking at
		if not day in schedule.keys():
			day_timeslots = schedule[day] = []

		# Get tutors in timeslot that actually match the course
		tutors = timeslot.tutor_set.filter(subjects__coursedept__iexact = course_dept, subjects__coursenum__iexact = course_num)

		day_timeslots.append({'halfhour': timeslot.halfhour, 'tutors': [tutor.name for tutor in tutors]})

	return schedule

def getScheduleJSON(date, course_dept, course_num):
	"""
	Gets a schedule from the database and nicely formats it in JSON for the frontend
	"""

	schedule = getSchedule(date, course_dept, course_num)

	return schedule