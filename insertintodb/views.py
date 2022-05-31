from django.shortcuts import render

from insertintodb.models import Insertintodb

# Create your views here.
def insert_into_db(Name, Roll_NUmber ,email, date, time):
    att_records = Insertintodb.objects.create(Name= Name,Roll_NUmber=Roll_NUmber, email = email,date= date, time = time)
    att_records.save()