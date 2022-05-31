from django.db import models

# Create your models here.
class Insertintodb(models.Model):
    Roll_NUmber = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=30)

    def __str__(self):
        return self.Roll_NUmber

    class Meta:
        db_table = 'student_records'
        verbose_name_plural = "Attendance Records"