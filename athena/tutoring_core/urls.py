from django.conf.urls import patterns, url

from tutoring_core import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='IndexView'),
    url(r'^ajax/search/courses$', views.CourseSearch.as_view(), name='CourseSearch'),
    url(r'^ajax/search/schedule/bycourse$', views.ScheduleSearch.as_view(), name='ScheduleSearch'),
)