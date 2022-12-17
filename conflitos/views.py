from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(request, 'pages/index.html', status=200, context={})

def grafics_page(request):
    ...

def lists_page(request):
    ...




