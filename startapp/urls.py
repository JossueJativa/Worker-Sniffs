from django.urls import path
from . import views

app_name = "startapp"

urlpatterns = [
    path("", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("ticket/<str:type_user>/", views.ticket, name="ticket"),
]