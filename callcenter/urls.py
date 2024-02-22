from django.urls import path
from . import views

app_name = "callcenter"

urlpatterns = [
    path('', views.index, name='index'),
    path('create_client/', views.create_client, name='create_client'),
    path('update_client/', views.update_client, name='update_client'),
    path('delete_client/<int:id>/', views.delete_client, name='delete_client'),
]