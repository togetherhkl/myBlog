# -*cding:utf-8-*-
from django.shortcuts import HttpResponse,redirect,render
from django import forms
from blog import models

class FCategoryModle(forms.ModelForm):
    class Meta:
        model=models.FCategory
        fields='__all__'
def home_display(request):
    '''首页展示'''
    #获取父级类的名字做菜单
    fcategories=models.FCategory.objects.all()
    categories=[]#父分类菜单
    #找出每个分类下的子分类
    for obj in fcategories:
        categorie = []#临时子分类
        category=models.Category.objects.filter(fcategory_id=obj.id)#某个分类的所有子分类
        for obj2 in category:
            categorie.append(obj2.category_name)#把名字放入一个列表
        categories.append(categorie)#把父类的子类放入列表
    #print(categories)
    categories.reverse()#反转一下便于前端输出
    #print(categories)

    content={
        'menu':fcategories,
        'category':categories
    }
    return render(request,'header_nav.html',content)
