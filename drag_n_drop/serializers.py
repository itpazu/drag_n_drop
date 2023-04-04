from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo

# run is valid on incoming data to validate the input and enable buttons
# dates not working properly
# join tables on foreign key before serializing


class UserSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Todo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'todos']


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description',
                  'created_at', 'completed', 'user']
