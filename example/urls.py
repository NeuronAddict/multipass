from django.urls import path

from . import views

urlpatterns = [

    # index view to client code that execute brute force
    path('login/', views.login, name='login'),

]
