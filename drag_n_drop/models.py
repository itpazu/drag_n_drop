from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone


class Todo(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.description

    class Meta:
        ordering = ['created_at']


class Changes(models.Model):
    EDIT = 'Edited item'
    NEW = 'Added new item'
    DELETED = 'Deleted item'
    USER_ACTIONS = [('edit', EDIT),
                    ('new', NEW),
                    ('deleted', DELETED)
                    ]
    old_item = models.TextField("previous entry", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_item = models.ForeignKey(Todo,  on_delete=models.CASCADE, blank=True)
    change_time = models.DateTimeField(auto_now_add=True)
    # implement changes with choices https://docs.djangoproject.com/en/4.1/ref/models/fields/
    change = models.CharField(choices=USER_ACTIONS, max_length=50, default=NEW)
