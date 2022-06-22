from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(r'index', views.index, name='index'),
    path(r'', views.home, name='home'),
    path(r'graph', views.graph, name='graph'),
]
