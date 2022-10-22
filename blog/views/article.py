# -*cding:utf-8-*-
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from blog import models


def article_show(request):
    '''返回某个分类下所有文章的文章信息'''
    if request.method=="GET":
        # print(request.GET)
        category=request.GET.get('category_id')
        category=int(category)
        queryset=models.Articles.objects.filter(category_id=category).all()
        # print(queryset)
        return render(request,'articles_show.html',{'objs':queryset})

def article_gettags(request):
    '''获取某篇文章的所有标签'''
    article_id=request.POST.get('article_id')
    article_id=int(article_id)
    quryset=models.TagSetArticle.objects.filter(article_id=article_id).all()
    tags=[]
    status=400
    for item in quryset:
        tag_id=item.tag_id
        tag_name=models.Tag.objects.filter(id=tag_id).first().tag_name
        tags.append(tag_name)
        status=200
    print(tags)
    data={
        'tags':tags,
        'status':status
    }
    return JsonResponse(data)

def article_show_page(request,nid):
    '''返回文章的html代码共前端解析'''
    #bug思考，这里会导致越权访问，如果用户不止一个，他在这上面发表了文章，但是他又不想给别人看。
    #这里通过修改前端get中的数字就可以越权访问到别人的文章
    article_id=nid
    obj=models.Articles.objects.filter(id=article_id).first()
    if not obj:
        status=400
        msg="文章不存在"
        # page=''
    else:
        status=200
        # page=obj.article_content
        msg=''
    data={
        # 'page':page,
        'status':status,
        'msg':msg,
        'article_id':article_id,
    }
    return render(request,'article_show_page.html',data)

def article_get_content(request):
    '''获取博客文章的具体内容'''
    article_id=request.POST.get('page_id')
    article_id=int(article_id)
    obj = models.Articles.objects.filter(id=article_id).first()
    page = obj.article_content
    print(page)
    data = {
        'page': page,
        'msg': 'success',
    }
    return JsonResponse(data)


#下面是测试的例子
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
@xframe_options_sameorigin
def article_test(request):
    obj = models.Articles.objects.filter(id=15).first()
    page=obj.article_content
    print(page)
    return render(request,'test.html',{'page':page})


@xframe_options_sameorigin
def article_test_getpage(request):
    obj = models.Articles.objects.filter(id=11).first()
    page = obj.article_content
    print(page)
    data={
        'page':page,
        'msg':'success',
    }
    return JsonResponse(data)





