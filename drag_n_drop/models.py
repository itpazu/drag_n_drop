from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)
    user = models.ForeignKey(
        'auth.User', related_name="todos", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-order', '-created_at']
