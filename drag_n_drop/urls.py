from django.urls import path, include

from . import views

urlpatterns = [
    path("register", views.UserCreate.as_view(), name="register"),
    path("auth_api", include('rest_framework.urls')),
    path("todos", views.UserTodos.as_view(), name="user_todos"),
    path("modify",
         views.ModifyTodos.as_view(), name="modify_todos")
]
