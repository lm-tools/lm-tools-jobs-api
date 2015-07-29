from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

from jobs_api import views


urlpatterns = patterns(
    '',
    url(r'dummy', views.DummyDashboardView.as_view(), name="dummy_api_view"),
    url(r'top_categories', views.TopCategoriesView.as_view(),
        name="top_categories_view"),
    url(r'top_companies', views.TopCompaniesView.as_view(),
        name="top_companies_view"),
    url(r'jobadverts', views.JobAdvertsView.as_view(),
        name="job_adverts_view"),
)
