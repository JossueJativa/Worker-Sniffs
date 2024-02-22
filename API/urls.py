# Importaciones del programa
from . import views

# Django
from django.urls import path, include

# Rest Framework
from rest_framework import routers

router = routers.DefaultRouter()

router.register('comments', views.CommentsViewSet)
router.register('stars', views.StarsViewSet)
router.register('product', views.ProductViewSet)
router.register('problems', views.ProblemsViewSet)
router.register('problems_tikets', views.Problems_TiketsViewSet)
router.register('client', views.ClientViewSet)
router.register('certificate', views.CertificateViewSet)
router.register('tecnic', views.TecnicViewSet)
router.register('manager', views.ManagerViewSet)
router.register('callcenter', views.CallCenterViewSet)
router.register('user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]