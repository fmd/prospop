from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render

def show_404(request):
    return render(request, '404.html', {})

def show_500(request):
    return render(request, '500.html', {})