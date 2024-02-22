from django.urls import path
from . import views

app_name = 'tecnic'

urlpatterns = [
    path('', views.intro, name='intro'),
    path('client/<int:id>', views.client, name='client'),
    path('change_status/<int:id>', views.change_status, name='change_status'),
    path('configuration', views.configuration, name='configuration'),
]