from django.db import models


class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=150)
    category = models.CharField(max_length=30, null=True)