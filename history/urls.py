from django.conf.urls import url
from . import views



urlpatterns  ={
    url(r'^(?P<mem_num>[0-9]+)/$',views.index, name='index'),
    url(r'^(?P<mem_num>[0-9]+)/comments/(?P<vin_num>[0-9]+)/$', views.comments, name='comments'),
}