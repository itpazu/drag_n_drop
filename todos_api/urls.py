from django.urls import path, include
from knox import views as knox_views
from . import views

urlpatterns = [
    # path("api/auth/login/", views.LoginView.as_view(), name='knox_login'),
    path("api/auth/", include('knox.urls')),
    path('api/auth/login', views.LoginView.as_view(), name='knox_login'),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path("api/auth/register", views.UserCreate.as_view(), name="register"),
    path("api/auth/user", views.AuthenticatedUser.as_view(), name="user"),
    path('api/auth/logoutall', knox_views.LogoutAllView.as_view(),
         name='knox_logoutall'),
    path('api/auth/user', knox_views.LogoutAllView.as_view(),
         name='get_user'),
    # path("api/auth/", include('knox.urls')),
    path("todos", views.UserTodos.as_view(), name="user_todos"),
    path("modify",
         views.ModifyTodos.as_view(), name="modify_todos")
]
