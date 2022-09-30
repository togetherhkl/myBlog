# -*cding:utf-8-*-
from django.shortcuts import HttpResponse,redirect,render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django import forms
from blog import models

@csrf_exempt
def create_article(request):
    '''写文章'''
    # return render(request,'create_article.html')
    return render(request, 'create_article.html')
    # return render(request, 'test.html')