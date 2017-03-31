from django.conf.urls import url
from . import views

urlpatterns  ={
    url(r'^$',views.adminCars, name='login'),
    url(r'^members/$', views.adminMembers, name='login'),
    url(r'^members/statement/(?P<mem_num>[0-9]+)/$', views.statement, name ='statement'),
    url(r'^rentalHistory/(?P<car_num>[0-9]+)/$', views.rentalHistory, name='rentalHistory'),
    url(r'^addCar/$', views.addCar, name='addCar'),
    url(r'^reservations/$', views.reservations, name='reservations'),
    url(r'^invoices/$', views.invoices, name='invoices'),
    url(r'^damaged/$', views.damaged, name='damaged'),
    url(r'^sort-by-rentals/$', views.sortByRentals, name='sortByRentals'),
    url(r'^searchByLocation/$', views.searchByLocation, name='searchByLocation'),
    url(r'^searchByLocation/(?P<location_num>[0-9]+)/$', views.carsByLocation, name='carsByLocation')
}