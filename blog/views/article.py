# -*cding:utf-8-*-
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from blog import models
def article_show(request):
    if request.method=="GET":
        print(request.GET)
        category=request.GET.get('category_id')
        category=int(category)
        queryset=models.Articles.objects.filter(category_id=category).all()
        print(queryset)
        return render(request,'articles_show.html',{'objs':queryset})
