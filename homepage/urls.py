from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('capture', views.capture, name='capture'),
    path('TakeSnapshotAndSave', views.TakeSnapshotAndSave, name='TakeSnapshotAndSave'),
    path('upload', views.upload, name='upload'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('download', views.download, name='download'),
    path('mobile', views.mobile, name='mobile'),
    path('mobileUP', views.mobileUP, name='mobileUP'),
    path('password_reset', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]