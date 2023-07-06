from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'material-type', MaterialTypeViewSet, basename='types')

urlpatterns = [
    path('', views.index, name='home'),
    path('api/wall/materials/', MaterialsAPIView.as_view()),
    path('api/wall/materials/<int:pk>/', MaterialsAPIView.as_view()),
    path('api/wall/producers/', ProducersAPIList.as_view()),
    path('api/wall/producers/<int:pk>/', ProducersAPIUpdate.as_view()),
    path('api/wall/producers-detail/<int:pk>/', ProducersAPIDetailView.as_view()),
    path('api/wall/', include(router.urls)),

    # path('materials', views.materials, name='materials'),
    # path('producers/', views.producers, name='producers'),
    path('calculations/', views.calculations, name='calculations'),
    path('office', views.private_office, name='office'),
]
