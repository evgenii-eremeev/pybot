from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Query(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    question = models.TextField(max_length=1000)
    answer = models.TextField(max_length=1000)

    def __str__(self):
        return self.question

