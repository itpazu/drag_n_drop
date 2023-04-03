from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("todos/<int:user_id>", views.user_todos, name="user_todos")
]
