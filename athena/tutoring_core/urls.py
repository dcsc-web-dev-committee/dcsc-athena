from django.conf.urls import patterns, url

from tutoring_core import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='IndexView'),
    url(r'^ajax/search$', views.AjaxSearch.as_view(), name='AjaxSearch'),
)