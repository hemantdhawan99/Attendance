from turtle import mode
from django.db import models

# Create your models here.

class Homepage(models.Model):
    Roll_NUmber = models.CharField(max_length=30, primary_key=True)
    Name = models.CharField(max_length=30)
    Image_Vector = models.TextField()
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Roll_NUmber

    class Meta:
        db_table = 'students'
        verbose_name_plural = "Student Records"