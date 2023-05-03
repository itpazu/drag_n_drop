from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, UserSerializer, ListTodoSerializer
from rest_framework import generics, permissions
from .permissions import IsOwner
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]


class AuthenticatedUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        print(self.request.user)
        return self.request.user


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })


class UserTodos(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class ModifyTodos(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    serializer_class = TodoSerializer
    serializer_list = ListTodoSerializer
    lookup_field = "id"

    def get_queryset(self, ids=None):
        if ids:
            return Todo.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(ModifyTodos, self).get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        ids = validate_ids(request.data)
        instances = self.get_queryset(ids=ids)
        data = request.data if isinstance(
            request.data, list) else [request.data]

        serializer = self.get_serializer(
            instances, data=data,  partial=True,  many=True, **kwargs
        )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


def validate_ids(data, field="id"):

    if isinstance(data, list):
        return [int(x.get(field)) for x in data if x.get(field, None) is not None]

    return [data]
