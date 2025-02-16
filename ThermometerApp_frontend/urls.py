# from django.conf.urls import url
from django.urls import re_path as url
from . import views

app_name = ''
urlpatterns = [
    url(r'^$', views.last_24h, name='last_24h'),
    url(r'^last_hour', views.last_hour, name='last_hour'),
    url(r'^specific_date', views.render_specific_day, name='specific_date'),
    url(r'^month_overview', views.render_month_overview, name='month_overview'),
    url(r'^all_reads', views.all_reads, name='all_reads'),
    url(r'^is_updated', views.is_updated, name='is_updated'),
]
