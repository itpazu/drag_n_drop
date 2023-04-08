from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# run is valid on incoming data to validate the input and enable buttons
# dates not working properly
# join tables on foreign key before serializing


class UserSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Todo.objects.all())
    password = serializers.CharField(
        write_only=True, required=True,  validators=[validate_password])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'todos', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description',
                  'created_at', 'completed', 'user', 'updated_at', 'order']
