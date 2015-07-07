from django.conf.urls import patterns, include, url

from jobs_api import  views

urlpatterns = patterns(
    '',
    url(r'dummy', views.DummyDashboardView.as_view(), name="dummy_api_view"),
    url(r'jobs_in_area', views.LatestJobsInArea.as_view(), name="jobs_in_area"),
)
