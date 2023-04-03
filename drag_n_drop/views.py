import os
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer


# from rest_framework.renderers import JSONRenderer

# apply login required
# get id from url or from body
# apply foreign key of user into todo seralizer or create
# @csrf_exempt


def index(request):
    print(os.environ['TZ'])
    todos = Todo.objects.all()  # filter for userId
    serialized = TodoSerializer(todos, many=True)
    # print(serialized)
    # output = JSONRenderer().render(serialized.data)
    return JsonResponse(serialized.data, safe=False)


# need to check if user e
@api_view(['GET', 'POST'])
def user_todos(request, user_id):
    try:
        # todos = Todo.objects.filter(user_id=user_id)
        user = User.objects.get(id=user_id)
        todos = user.todo_set.all()
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        todo = user.todo_set.create(**serializer.data)
        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE', 'PUT'])
# def modify_or_delete_todo(request, todo_id):
#     try:
#             # todos = Todo.objects.filter(user_id=user_id)
#             todo = Todo.objects.get(pk=todo_id)
#     except User.DoesNotExist:
#         return HttpResponse(status=404)
#  if request.method == 'PUT':
#         serializer = TodoSerializer(todos, data=request.data)
#         if serializer.is_valid():
#             print(serializer.data)
#             response = user.todo_set.create(serializer)
#             # serializer.save()
#             return JsonResponse(TodoSerializer(response, data=response))
#         return JsonResponse(serializer.errors, status=400)

# elif request.method == 'DELETE':
#         todos.delete()
#         return HttpResponse(status=204)
