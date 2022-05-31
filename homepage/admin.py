from django.contrib import admin
from .models import Homepage
from django import forms
# Register your models here.

class MyChangeForm(forms.ModelForm): 

    def __init__(self, *args, **kwargs): 
        super(MyChangeForm, self).__init__(*args, **kwargs)                       
        self.fields['Image_Vector'].disabled = True

@admin.register(Homepage)
class HomepageAdmin(admin.ModelAdmin):
    form = MyChangeForm
    list_display = ("Roll_NUmber", "Name" , "email")