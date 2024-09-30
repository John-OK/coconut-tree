from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core import serializers

def send_the_homepage(request):
    print('home')
    theIndex = open('static/index.html').read()
    return HttpResponse(theIndex)