from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user


class ListTodoSerializer(serializers.ListSerializer):

    def update(self, instances, validated_data):

        modify_items_dic = [
            (item.get("id"), item) for item in validated_data]
        db_instances_dic = {instance.id: instance for
                            instance in instances}

        update_dic = []
        for todo_id, fields in modify_items_dic:
            print(todo_id, fields)
            dbItem = db_instances_dic.get(todo_id, None)
            if dbItem is None:
                update_dic.append(self.child.create(fields))
            elif fields.get("description", '') == "delete":
                dbItem.delete()
            else:
                update_dic.append(self.child.update(dbItem, fields))
        return update_dic


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description',
                  'completed', 'order', 'user', 'created_at', 'updated_at']
        list_serializer_class = ListTodoSerializer
