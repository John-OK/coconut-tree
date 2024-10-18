from django.shortcuts import render
from django.http import HttpResponse

def orders(request):
    return HttpResponse('<h1>HELLO!</h1>')
