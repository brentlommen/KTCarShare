from django.conf.urls import url
from . import views

urlpatterns  ={
    #/cars/
   # url(r'^$',views.index, name='index'),

    #/cars/memNum

    url(r'^(?P<mem_num>[0-9]+)/$', views.index, name='index'),

    #/cars/id

    url(r'^(?P<mem_num>[0-9]+)/(?P<car_id>[0-9]+)/$', views.details, name='detail'),
    url(r'^(?P<mem_num>[0-9]+)/(?P<car_id>[0-9]+)/booking/$', views.booking, name='booking')



}