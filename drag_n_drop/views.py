import os
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwner


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserTodos(generics.ListCreateAPIView):
    # queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class ModifyTodos(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
