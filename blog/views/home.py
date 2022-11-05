# -*cding:utf-8-*-
from django.shortcuts import HttpResponse,redirect,render
from django.core import serializers  # 引入序列化器
from django.http import JsonResponse
from django.db.models import Q, Count  # 引入Q查询，也就是多条件查询,和聚合函数count
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
    if request.method=="GET":
        return render(request,'home_display.html')
    if request.method=="POST":
        # 获取top的前六篇文章
        if request.POST.get('type') == 'get_article_top':
            data = {}
            temp = models.Articles.objects.filter(article_top=1,user_id=1).all().order_by('-id')[0:6]
            data['article_set'] = serializers.serialize('json', temp)
            return JsonResponse(data)
        # 构造柱状图前端数据
        if request.POST.get('type') == 'barchar':
            # 获取分类的id和name
            # xAxis_data = list(models.Category.objects.values_list('id','category_name', flat=True))
            xAxis = list(
                models.Category.objects.filter(user_id=1).values('id', 'category_name'))
                #默认显示xh的文章，如果后期考虑别人使用则需要设置为登录者的id
            # print(xAxis)
            # 聚合查询，查询出对应分类且为共享的文章数目
            temp = models.Articles.objects.filter(user_id=1,article_auth=1).values('category_id').annotate(
                total=Count('id'))
            # select category,count(id) as total from Articles where user_id=id group by category
            # 构造数据分析的字典
            xAxis_data = []
            series_data = []
            temp2 = []  # 存储未分类
            for x in xAxis:
                xAxis_data.append(x['category_name'])
                total = 0
                for count in temp:
                    if count['category_id'] == None:
                        temp2.append('未分类')
                        temp2.append(count['total'])
                    elif count['category_id'] == x['id']:
                        total = count['total']
                x['total'] = total
            data = {
                'msg': 'yes',
            }
            for x in xAxis:
                series_data.append(x['total'])
            # 添加未分类数据
            xAxis_data.append(temp2[0])
            series_data.append(temp2[1])
            data['xAxis_data'] = xAxis_data
            data['series_data'] = series_data
            return JsonResponse(data)
        #如果是获取最新的文章
        if request.POST.get('type')=='latest':
            data={}
            temp = models.Articles.objects.filter(user_id=1,article_auth=1).all().order_by('-article_updatedate')[0:10]
            data['latest']=serializers.serialize('json', temp)
            return JsonResponse(data)
        #获取收藏量多的文章
        if request.POST.get('type')=='popular':
            data={}
            temp = models.Articles.objects.filter(user_id=1,article_auth=1).all().order_by('-article_collect')[0:10]
            data['popular']=serializers.serialize('json', temp)
            return JsonResponse(data)
        return render(request, 'home_display.html')

