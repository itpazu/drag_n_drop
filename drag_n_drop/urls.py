from django.urls import path, include

from . import views

urlpatterns = [
    # path("", views.index, name="index"),

    path("auth_api/", include('rest_framework.urls')),
    path("todos/", views.UserTodos.as_view(), name="user_todos"),
    path("modify/<int:pk>",
         views.ModifyTodos.as_view(), name="modify_todos"),
]
