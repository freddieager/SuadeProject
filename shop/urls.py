from django.urls import path
from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r'report/(?P<date>\d{4}-\d{2}-\d{2})/$', views.ReportView.as_view(), name='report_view'),
]
