# -*cding:utf-8-*-

from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django.utils import timezone
from django import forms
from blog import models


class ArticlesModleForm(forms.ModelForm):
    '''文章类的modelform'''
    class Meta:
        model = models.Articles
        fields = ['article_title', 'article_digest', 'category', 'article_top', 'article_img', 'article_auth', 'tag']
        # fields='__all__'
        widgets = {
            'article_digest': forms.Textarea(attrs={'placeholder':'输入四百字内的摘要'}),
            'article_img': forms.TextInput,
        }
        labels={
            'article_img':'文章封面'
        }

def create_article(request):
    '''写文章与保存文章'''
    # return render(request,'create_article.html')
    if request.method=="GET":
        form = ArticlesModleForm()
        context = {
            'form': form,
        }
        return render(request, 'create_article.html', context)
    #POST提交博客文章数据
    form = ArticlesModleForm(data=request.POST)
    data={}
    if form.is_valid():
        # print(request.POST)
        title=request.POST.get('article_title')
        digest=request.POST.get('article_digest')
        top=request.POST.get('article_top')
        img=request.POST.get('article_img')
        auth=request.POST.get('article_auth')
        content=request.POST.get('article_data')
        status=request.POST.get('article_status')
        category=None
        tag=None
        if request.POST.get('category'):
            category=request.POST.get('category')
            category=int(category)
        if request.POST.get('tag'):
            tag=request.POST.get('tag')
            tag=int(tag)
        # print(request.session['info']['id'])
        #前端选择保存
        if status=='2':
            models.Articles.objects.create(
                user_id=request.session['info']['id'],
                article_title=title,
                article_digest=digest,
                article_top=top,
                article_img=img,
                article_auth=0,
                article_content=content,
                category_id=category,
                tag_id=tag,
                article_updatedate=timezone.now()
            )
            data['msg']='发表成功，等待审核'
            data['status']=200
        elif status=='1':
            models.Articles.objects.create(
                user_id=request.session['info']['id'],
                article_title=title,
                article_digest=digest,
                article_top=top,
                article_img=img,
                article_auth=auth,
                article_content=content,
                category_id=category,
                tag_id=tag,
                article_updatedate=timezone.now(),
                article_status=1
            )
            data['msg'] = '保存成功'
            data['status'] = 200
    else:
        print(form.errors)
        data['msg']=form.errors
        data['status']=400
    return JsonResponse(data)



def create_punlis(request):
    '''发表文章模态框所需要的数据'''
    #获取父分类
    Fcatagory = models.FCategory.objects.all()
    fcatagory = []
    for obj in Fcatagory:
        tem=[]
        tem.append(obj.id)
        tem.append(obj.fcategory_name)
        fcatagory.append(tem)
    #获取子分类
    catagory=[]
    status=True
    if request.POST.get('fcatagory_id'):
        id=request.POST.get('fcatagory_id')
        catagory_dict=models.Category.objects.filter(fcategory_id=id).all()
        if catagory_dict:
            for item in catagory_dict:
                tem2=[]
                tem2.append(item.id)
                tem2.append(item.category_name)
                catagory.append(tem2)
            print(catagory)
        else:
            status=False
    #获取父标签
    ftag_dict=models.FTag.objects.all()
    ftag=[]
    for obj in ftag_dict:
        tem3=[]
        tem3.append(obj.id)
        tem3.append(obj.ftag_name)
        ftag.append(tem3)
    #获取子标签
    status2=True
    tag=[]
    if request.POST.get('ftag_id'):
        id=request.POST.get('ftag_id')
        tag_dict=models.Tag.objects.filter(ftag_id=id).all()
        if tag_dict:
            for obj in tag_dict:
                tem=[]
                tem.append(obj.id)
                tem.append(obj.tag_name)
                tag.append(tem)
            print(tag)
        else:
            status2=False
    context={
        'fcatagory':fcatagory,
        'catagory':catagory,
        'status':status,
        'ftag':ftag,
        'tag':tag,
        'status2':status2,
    }
    return  JsonResponse(context)

