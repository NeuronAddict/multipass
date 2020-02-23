from django.urls import path

from . import views

urlpatterns = [

    # index view to client code that execute brute force
    path('<domain>/', views.index, name='index'),

    # exfiltration of username/password
    path('<domain>/exfiltrate/', views.exfiltrate, name='exfiltrate'),

    # get list of non ack probes
    path('<domain>/probes/', views.probes, name='probes'),

    # POST the tested username offset
    path('<domain>/ack/', views.ack, name='ack'),

]
