from django.db import models

# Create your models here.


class Todo(models.Model):
    title=models.CharField(max_length=200)
    created_date=models.DateField(auto_now_add=True,blank=True)
    user=models.CharField(max_length=200)
    options=(
        ("completed","completed"),
        ("pending","pending"),
        ("inprogress","inprogress")
    )
    status=models.CharField(max_length=200,choices=options,default="pending")


    def __str__(self):
        return self.title