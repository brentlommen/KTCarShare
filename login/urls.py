from django.conf.urls import url
from . import views

urlpatterns  ={
    url(r'^$',views.get_login, name='login'),
    url(r'^signup/$', views.signUp, name='signup')
}