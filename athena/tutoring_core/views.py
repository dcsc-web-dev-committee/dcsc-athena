from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse

import datetime as dt

from tutoring_core import schedulesearch

# Create your views here.
class IndexView(View):
	def get(self, request):
		return HttpResponse("Hello World!")

class AjaxSearch(View):
	def get(self, request):
		try:
			course_dept = 	request.GET['course_dept']
			course_num = 	request.GET['course_num']
			date_year = 	int(request.GET['date_year'])
			date_month = 	int(request.GET['date_month'])
			date_day = 		int(request.GET['date_day'])
		except KeyError:
			return JsonResponse({'status': {'type': 'error', 'reason': 'missing_params',}}, status = 400)
		except ValueError:
			return JsonResponse({'status': {'type': 'error', 'reason': 'bad_params',}}, status = 400)

		query_date = dt.date(date_year, date_month, date_day)
		schedule_results = schedulesearch.getScheduleJSON(query_date, course_dept, course_num)

		return JsonResponse({'status': {'type': 'success'}, 'week_results': schedule_results})