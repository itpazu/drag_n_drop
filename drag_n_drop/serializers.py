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
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=True, min_length=5, max_length=150)
    # description = serializers.CharField()
    # created_at = serializers.DateTimeField()
    # completed = serializers.BooleanField(default=False)
    # user = serializers.IntegerField(required=True)
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'created_at', 'completed']

    # def create(self, validated_data):

    #     return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print('instance', instance.description)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.completed = validated_data.get(
            'completed', instance.completed)
        instance.save()
        return instance
