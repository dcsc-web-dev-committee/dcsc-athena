from tutoring_core import models

import datetime as dt

def getCourses(course_dept, course_num):
	"""
	Performs heavy lifting of core database queries
	"""

	courses = models.Course.objects.filter(dept__iexact = course_dept, num__iexact = course_num)

	results = [{'course_id': course.id, 'dept': course.dept.upper(), 'num': course.num.upper(), 'name': course.getTitleName()} for course in courses]

	return results