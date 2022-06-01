import csv
import datetime
from email import message
import re
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpRequest
from cgitb import grey
import os
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from cv2 import cv2
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from imageio import imread
from skimage.transform import resize
from scipy.spatial import distance
import tensorflow as tf
from homepage.models import Homepage
from insertintodb.models import Insertintodb
from insertintodb.views import insert_into_db
from tensorflow.keras.models import load_model
from utils import image_embedding
from utils import db_extraction
from django.core.mail import send_mail
from django.contrib import messages, auth
from django.http import HttpResponse
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


#import the cascade for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def Home(request):
    return render(request, 'pages/home.html')

def TakeSnapshotAndSave(request):
    # try:
    # access the webcam (every webcam has a number, the default is 0)
        path ='Dataset/Images'
        cap = cv2.VideoCapture(0)
        timeout = 5   # [seconds]

        timeout_start = time.time()

        while time.time() < timeout_start + timeout:
            test = 0
            if test == 5:
                break
            test -= 1

            # Capture frame-by-frame
            ret, frame = cap.read()
            
            # to detect faces in video
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)


            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                

            x = 200
            y = 20
            text_color = (0,255,0)
            # write on the live stream video
            cv2.putText(frame, "Please wait for 3 seconds", (x,y), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=2)


            # Display the resulting frame
            cv2.imshow('frame',frame)
            # press the letter "q" to save the picture
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                # write the captured image with this name
            
        cv2.imwrite(os.path.join(path , 'IM12.jpg'),frame)
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        return capture(request)
    # except:
    #     clear_dir()
    #     messages.warning(request, 'Something went wrong, please try again.')
    #     return render(request, 'pages/home.html')


def capture(request):
    try:
        path1='Dataset/Images'
        embeddings=image_embedding.generate_image_encoding(path1)
        global k
        k=db_extraction.get_student(embeddings)
        if k==('Not Found','Not Found','Not Found'):
            clear_dir()
            return render(request,'pages/notfound.html')
        else:
            current_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            current_date = datetime.date.today().strftime('%d/%m/%Y')
            context= {
                'name':k[1],
                'roll':k[0]
                }
            send_mail(
            'NeuroMarking',
            'Dear '+ k[1] +', your attendance has been marked at '+ current_time +' on '+ current_date + '.',
            'nexuslandholdings@gmail.com',
            [k[2]],
            )
            insert_into_db(k[1], k[0], k[2], current_date, current_time)
            clear_dir()
            return render(request,'pages/present.html',context)  
    except:
        clear_dir()
        messages.error(request, 'Something went wrong, please try again.') 
        return render(request, 'pages/home.html')

def clear_dir():
    dir = 'Dataset/Images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            image = request.FILES['image']
            Name = request.POST['name']
            Roll_NUmber = request.POST['rollnumber']
            email = request.POST['email']
            if Homepage.objects.filter(Roll_NUmber=Roll_NUmber).exists():
                messages.warning(request, 'Record already exists!')
                return render(request, 'pages/upload.html')
            else:
                with open('Dataset/Upload/img.jpg', 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                return upload_to_db(request, Roll_NUmber, Name, email)
    else:
        messages.warning(request, 'Please login!')
        return render(request, 'pages/admin.html')

def upload_to_db(request , Roll_NUmber, Name, email):
    try:
        path = 'Dataset/Upload'
        embeddings=image_embedding.generate_image_encoding(path)
        embeddings=embeddings.tolist()
        newEmb = str(embeddings)
        upload1 = Homepage.objects.create(Roll_NUmber=Roll_NUmber, Name = Name,  Image_Vector=newEmb, email= email)
        upload1.save()
        clear_uploadDir()
        messages.success(request, 'Data Uploaded Successfully!')
        return render(request, 'pages/upload.html')
    except:
        clear_uploadDir()
        messages.warning(request,'Some error occured')
        return render(request, 'pages/upload.html')

def clear_uploadDir():
    dir = 'Dataset/Upload'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return render(request, 'pages/upload.html')
        else:
            messages.warning(request, 'Invalid credentials')
            return render(request,'pages/admin.html')
    else:
        return render(request, 'pages/admin.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return render(request, 'pages/admin.html')

def download(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['Name', 'Roll Number', 'Email', 'Date', 'Time'])

        for member in Insertintodb.objects.all().values_list('Name', 'Roll_NUmber' , 'email', 'date', 'time'):
            writer.writerow(member)
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
        return response
    else:
        messages.warning(request, 'Operation not allowed.')
        return render(request, 'pages/admin.html')

def notfound(request):
    return render(request, 'pages/notfound.html')

def mobile(request):
    return render(request, 'pages/mobile.html')

def mobileUP(request):
    try:
        if request.method == 'POST':
            image = request.FILES['image']
            with open('Dataset/Images/img.jpg', 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
            return capture(request)
    except:
        messages.warning(request, "Some error occured!")
        return render(request, 'pages/mobile.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "Password reset initiated. Check your email."
    success_url = 'login'