from django.urls import path
from . import views

app_name = "manager"

urlpatterns = [
    path("", views.principal_page, name="principal_page"),
    path("workers/", views.workers, name="workers"),
    path("delete_worker/<int:id>", views.delete_worker, name="delete_worker"),
    path("edit_worker/", views.edit_worker, name="edit_worker"),
    path("block_worker/<int:id>", views.block_worker, name="block_worker"),
    path("unblock_worker/<int:id>", views.unblock_worker, name="unblock_worker"),
    path("clients/", views.clients, name="clients"),
    path("accept_client/<int:id>", views.accept_client, name="accept_client"),
    path("reject_client/<int:id>", views.reject_client, name="reject_client"),
]