from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    print('LOADING HOMEPAGE')
    return HttpResponse("HELLO WORLD!")