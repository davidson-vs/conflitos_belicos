from django.urls import path
from conflitos.views import homepage


urlpatterns = [
    path('', homepage) 
]