import imp
from django.contrib import admin
from .models import Insertintodb
from django import forms

class MyChangeForm2(forms.ModelForm): 

    def __init__(self, *args, **kwargs): 
        super(MyChangeForm2, self).__init__(*args, **kwargs)                       
        self.fields['Roll_NUmber'].disabled = True
        self.fields['Name'].disabled = True
        self.fields['email'].disabled = True
        self.fields['date'].disabled = True
        self.fields['time'].disabled = True


@admin.register(Insertintodb)
class InsertintodbAdmin(admin.ModelAdmin):
    form = MyChangeForm2
    list_display = ("Roll_NUmber", "Name" , "email", "date")
    search_fields = ("Roll_NUmber__startswith", )