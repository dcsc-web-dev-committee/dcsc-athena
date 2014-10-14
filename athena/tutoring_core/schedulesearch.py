from tutoring_core import models

import datetime as dt

def getWeekDays(date):
	"""
	Given a datetime.date, return a list of the other datetime.date objects in the
	same Monday-based week
	"""

	weekday = date.weekday()
	return [date + dt.timedelta(days = offset) for offset in range(0 - weekday, 7 - weekday)]

def getScheduleDB(date, course_id):
	"""
	Performs heavy lifting of core database queries
	"""

	weekdays = getWeekDays(date)

	# First, get all WeeklyTimeSlots that have a Tutor who has a Course which matches the query 
	timeslots = models.WeeklyTimeSlot.objects.filter(tutor__courses = course_id)

	# Then, filter out Tutors who do not have an ActiveTerm within the query
	timeslots = timeslots.filter(tutor__terms__start__lte = date, tutor__terms__end__gte = date)

	# TODO: filter out WeeklyTimeSlots that exists outside the bounds of the ActiveTerm
	# TODO: check for TimeOffs
	# TODO: add MakeUp hours
	# TODO: check for holidays

	schedule = {}

	for timeslot in timeslots:
		# Get day and time in question
		day = timeslot.getDayAsString()

		# Set reference to which day we are looking at
		if not day in schedule.keys():
			day_timeslots = schedule[day] = []

		# Get tutors in timeslot that actually match the course
		tutors = timeslot.tutor_set.filter(courses = course_id)

		day_timeslots.append({'halfhour': timeslot.halfhour, 'tutors': [tutor.name for tutor in tutors]})

	return schedule

def getSchedule(date, course_id):
	"""
	Gets a schedule from the database and nicely formats it in JSON for the frontend
	"""

	schedule = getScheduleDB(date, course_id)

	return schedule