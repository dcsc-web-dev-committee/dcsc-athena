from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse

import abc
import datetime as dt

from tutoring_core import schedulesearch, coursesearch

# Create your views here.
class IndexView(View):
	def get(self, request):
		return HttpResponse("Hello World!")

class AjaxSearchView(View):
	__metaclass__ = abc.ABCMeta

	def get(self, request):
		try:
			self.checkGetRequestParams(request)
		except KeyError:
			return JsonResponse({'status': {'type': 'error', 'reason': 'missing_params',}}, status = 400)
		except ValueError:
			return JsonResponse({'status': {'type': 'error', 'reason': 'bad_params',}}, status = 400)

		result = self.doSearch()

		return JsonResponse(result, safe = False)

	@abc.abstractmethod
	def checkGetRequestParams(self):
		return

class CourseSearch(AjaxSearchView):
	def checkGetRequestParams(self, request):
		self.dept = request.GET['dept']
		self.num = 	request.GET['num']

	def doSearch(self):
		results = coursesearch.getCourses(self.dept, self.num)

		return {'status': {'type': 'success'}, 'courses': results}

class ScheduleSearch(AjaxSearchView):
	def checkGetRequestParams(self, request):
		self.course_id = 	int(request.GET['course_id'])
		self.year = 		int(request.GET['year'])
		self.month = 		int(request.GET['month'])
		self.day = 			int(request.GET['day'])

	def doSearch(self):
		query_date = dt.date(self.year, self.month, self.day)
		schedule_results = schedulesearch.getSchedule(query_date, self.course_id)

		return {'status': {'type': 'success'}, 'timeslots': schedule_results}