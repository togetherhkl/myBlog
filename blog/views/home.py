# -*cding:utf-8-*-
from django.shortcuts import HttpResponse,redirect,render
from django.http import JsonResponse
from django import forms
from blog import models

class FCategoryModle(forms.ModelForm):
    class Meta:
        model=models.FCategory
        fields='__all__'
def home_nav(request):
    '''首页展示'''
    #获取父级类的名字做菜单
    fcategories=models.FCategory.objects.all()
    categories=[]#储存分类菜单得名字
    fcat=[]#存储父类菜单的名字
    #找出每个分类下的子分类
    for obj in fcategories:
        categorie = []#临时子分类
        fcat.append(obj.fcategory_name)#获取父分类的名称
        category=models.Category.objects.filter(fcategory_id=obj.id)#某个分类的所有子分类
        for obj2 in category:
            temp=[]
            temp.append(obj2.category_name)
            temp.append(obj2.id)
            # print(temp)
            categorie.append(temp)#把名字放入一个列表
        categories.append(categorie)#把父类的子类放入列表
    # print(categories)
    content = {
        'menu': fcat,
        'category': categories
    }
    return JsonResponse(content)#json数据传输


def home_display(request):
    return render(request,'home_display.html')
