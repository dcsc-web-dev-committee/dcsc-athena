from django.db import models

import datetime as dt

# Create your models here.

class Tutor(models.Model):
	name = models.CharField(max_length = 100)
	bio = models.TextField()
	times = models.ManyToManyField('WeeklyTimeSlot')
	courses = models.ManyToManyField('Course')
	terms = models.ManyToManyField('ActiveTerm')

	def __str__(self):
		return '{0}'.format(self.name)

class Course(models.Model):
	# TODO: ensure only one object created per unqiue "value"

	name = models.CharField(max_length = 100)
	dept = models.CharField(max_length = 5)
	num = models.CharField(max_length = 5)

	def __str__(self):
		return '{0} {1} ({2})'.format(self.coursedept, self.coursenum, self.name)

	def getTitleName(self):
		return ' '.join(word[0].upper() + word[1:] for word in self.name.split(' ') if word)

# Normal schedule. Time slots are used instead of a datetime range for 
# regularity and conservation.
#
# When a schedule is rendered, it should render each time slot one by one.
# It will check all tutors availible and then check for ActiveTerm, 
# TimeOff, and Holiday conflicts.
# Lastly, any Makeups are rendered for the schedule's range

class WeeklyTimeSlot(models.Model):
	# TODO: ensure only one object created per unqiue "value"

	# From 0 (Monday) to 6 (Sunday)
	day = models.IntegerField()
	# From 0 (00:00 - 00:29) to 47 (23:30 - 23:59)
	halfhour = models.IntegerField()

	def __str__(self):
		return '{0}, {1}'.format(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][self.day], self.halfhour)

	def getDayAsString(self):
		return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][self.day]


# Below exists things beyond core functionality

# Describes the term (e.g; A UC Davis quarter) that a tutor will serve
class ActiveTerm(models.Model):
	name = models.CharField(max_length = 100)
	start = models.DateTimeField()
	end = models.DateTimeField()

	def __str__(self):
		return '{0}'.format(self.name)

# One off/special cases for when a tutor needs some time off
class TimeOff(models.Model):
	tutor = models.ForeignKey(Tutor)
	start = models.DateTimeField()
	end = models.DateTimeField()

# One off/special cases for when a tutor needs some time off
class Makeup(models.Model):
	tutor = models.ForeignKey(Tutor)
	start = models.DateTimeField()
	end = models.DateTimeField()

# Represents school holidays when one would expect that no tutors will work
# When a Holiday is created, all tutors will be added to it
# When a Tutor is created, they will be added to all existing Holidays
class Holiday(models.Model):
	tutors = models.ManyToManyField(Tutor)
	start = models.DateTimeField()
	end = models.DateTimeField()