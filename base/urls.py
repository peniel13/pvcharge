from django.urls import path
from . import views

urlpatterns = [
    
  path('',views.index, name= 'index'),
  path('apropos/', views.apropos, name='apropos'),

]


