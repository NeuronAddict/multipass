from django.urls import path

from . import views

urlpatterns = [
    path('<domain>/', views.index, name='index'),
    path('<domain>/exfiltrate/', views.exfiltrate, name='exfiltrate'),
    path('<domain>/usernames/', views.usernames, name='usernames'),
    path('<domain>/passwords/', views.passwords, name='passwords'),
]
