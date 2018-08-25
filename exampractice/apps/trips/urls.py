from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^home$',views.home, name='home'),
    url(r'^add$',views.add, name='add'),
    url(r'^entertrip$',views.entertrip, name='entertrip'),
    url(r'^new_destination/(?P<id>\w+)$',views.show, name='show'),
    url(r'^new_destination/(?P<id>\w+)/join$',views.join, name='join'),

]
