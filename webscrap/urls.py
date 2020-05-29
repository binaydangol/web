from webscrap import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='index'),
    path('corona', views.corona_info, name='info'),

]
