from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

from jobs_api import  views


router = DefaultRouter()
router.register(r'jobadverts', views.JobAdvertViewSet)


urlpatterns = patterns(
    '',
    url(r'dummy', views.DummyDashboardView.as_view(), name="dummy_api_view"),
    url(r'top_categories', views.TopCategoriesView.as_view(), name="top_categories_view"),
    url(r'^', include(router.urls)),
)
