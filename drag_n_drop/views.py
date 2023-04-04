import os
from django.contrib.auth.models import User
from django.http import Http404
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import generics


# from rest_framework.renderers import JSONRenderer

# apply login required
# get id from url or from body
# apply foreign key of user into todo seralizer or create


# def index(request):
#     print(os.environ['TZ'])
#     todos = Todo.objects.all()  # filter for userId
#     serialized = TodoSerializer(todos, many=True)
#     # print(serialized)
#     # output = JSONRenderer().render(serialized.data)
#     return JsonResponse(serialized.data, safe=False)


class UserTodos(APIView):

    def get_user(self, user_id):
        try:
            # todos = Todo.objects.filter(user_id=user_id)
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        user = self.get_user(user_id)
        todos = user.todos.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        user = self.get_user(user_id)
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            todo = user.todos.create(**serializer.data)
            return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModifyTodos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
