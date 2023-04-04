from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("todos/<int:user_id>", views.UserTodos.as_view(), name="user_todos"),
    path("modify/<int:pk>",
         views.ModifyTodos.as_view(), name="modify_todos")
]
