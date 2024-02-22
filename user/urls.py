from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('<int:identity>/', views.index, name='index'),
]