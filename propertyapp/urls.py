from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('addproperty/', views.addproperty, name='addproperty'),
    path('submitprop/', views.submitprop, name='submitprop'),
    re_path(r'^searchprop/$', views.searchprop, name='searchprop'),
    path('propdetails/<int:id>/', views.propdetails, name='propdetails'),
    


]