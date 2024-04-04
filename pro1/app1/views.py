from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    d = {'name': 'Arun', 'age': 21}
    return render(request,'home.html',d)
def index(request):
    return render(request,'index.html')

