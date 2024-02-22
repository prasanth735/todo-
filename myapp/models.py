from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Todo(models.Model):
    title=models.CharField(max_length=200)
    created_date=models.DateField(auto_now_add=True,blank=True)
    user_objects=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("completed","completed"),
        ("pending","pending"),
        ("inprogress","inprogress")
    )
    status=models.CharField(max_length=200,choices=options,default="pending")


    def __str__(self):
        return self.title