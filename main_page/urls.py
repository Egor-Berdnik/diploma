from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('materials', views.materials, name='materials'),
    path('producers/', views.producers, name='producers'),
    path('calculations', views.calculations, name='calculations'),
    path('office', views.private_office, name='office'),
]
