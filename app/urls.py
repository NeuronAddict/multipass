from django.urls import path

from . import views

urlpatterns = [

    # index view to client code that execute brute force
    path('<domain>/', views.index, name='index'),

    # exfiltration of username/password
    path('<domain>/exfiltrate/', views.exfiltrate, name='exfiltrate'),

    # get list of non ack usernames
    path('<domain>/usernames/', views.usernames, name='usernames'),

    # POST the tested username offset
    path('<domain>/usernames/ack', views.usernames, name='usernames'),

    # get list of non ack passwords
    path('<domain>/passwords/', views.passwords, name='passwords'),

    # POST the tested password offset
    path('<domain>/passwords/ack', views.usernames, name='usernames'),
]
