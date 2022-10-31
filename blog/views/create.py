# -*cding:utf-8-*-

from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django.utils import timezone
from django import forms
from blog import models


class ArticlesModleForm(forms.ModelForm):
    '''文章类的modelform'''
    tag = forms.CharField(label='标签', max_length=32, required=False)

    class Meta:
        model = models.Articles
        fields = ['article_title', 'article_digest', 'category', 'article_top', 'article_img', 'article_auth', 'tag']
        # fields='__all__'
        widgets = {
            'article_digest': forms.Textarea(attrs={'placeholder': '输入四百字内的摘要'}),
            'article_img': forms.TextInput,
        }
        labels = {
            'article_img': '文章封面'
        }


def create_article(request):
    '''写文章与保存文章'''
    # return render(request,'create_article.html')
    if request.method == "GET":
        form = ArticlesModleForm()
        data = {
            'form': form,
            'article_id': 'none',
            'option': 'create',
        }
        return render(request, 'create_article.html', data)
    # POST提交博客文章数据
    form = ArticlesModleForm(data=request.POST)
    data = {}
    if form.is_valid():
        # print(request.POST)
        title = request.POST.get('article_title')
        digest = request.POST.get('article_digest')
        top = request.POST.get('article_top')
        img = request.POST.get('article_img')
        auth = request.POST.get('article_auth')
        content = request.POST.get('article_data')
        status = request.POST.get('article_status')
        category = None
        tags = []  # 储存选择的标签
        flag = False  # 判度前端是否选择标签
        article_id=''
        # 如果前端选择了分类
        if request.POST.get('category'):
            category = request.POST.get('category')
            category = int(category)
        # 如果前端选择了标签
        if request.POST.get('tags'):
            flag = True
            temp = request.POST.get('tags')
            tags = temp.split(',')
        #如果前端是修改
        if request.POST.get('article_id'):
            article_id=request.POST.get('article_id')
        # print(request.session['info']['id'])
        # 前端选择发表
        if status == '2':
            temp = models.Articles.objects.create(
                user_id=request.session['info']['id'],
                article_title=title,
                article_digest=digest,
                article_top=top,
                article_img=img,
                article_auth=0,
                article_content=content,
                category_id=category,
                article_updatedate=timezone.now()
            )
            # 添加标签记录
            if flag:
                for i in tags:
                    models.TagSetArticle.objects.create(article_id=temp.id, tag_id=int(i))
            data['msg'] = '发表成功，等待审核'
            data['status'] = 200
        # 前端选择保存
        elif status == '1':
            temp = models.Articles.objects.create(
                user_id=request.session['info']['id'],
                article_title=title,
                article_digest=digest,
                article_top=top,
                article_img=img,
                article_auth=auth,
                article_content=content,
                category_id=category,
                article_updatedate=timezone.now(),
                article_status=1
            )
            # 添加标签到数据库
            if flag:
                for i in tags:
                    models.TagSetArticle.objects.create(article_id=temp.id, tag_id=int(i))
            data['msg'] = '保存成功'
            data['status'] = 200
        # 前端选择修改
        elif status == '3':
            models.Articles.objects.filter(pk=article_id).update(
                user_id=request.session['info']['id'],
                article_title=title,
                article_digest=digest,
                article_top=int(top),
                article_img=img,
                article_auth=int(auth),
                article_content=content,
                category_id=category,
                article_updatedate=timezone.now(),
                article_status=3,
            )
            # 更新标签记录
            models.TagSetArticle.objects.filter(article_id=article_id).delete()
            if flag:
                for i in tags:
                    models.TagSetArticle.objects.create(article_id=article_id,tag_id=int(i))
            data['msg'] = '更新成功，等待审核'
            data['status'] = 200
    else:
        # print(form.errors)
        data['msg'] = form.errors
        data['status'] = 400
    return JsonResponse(data)


def create_article_mod(request, nid):
    '''修改文章'''
    # 1.接受数据
    article_id = int(nid)
    # 1.1验证前端数据,防止数据错误
    # 2.返回前端界面
    if request.method == "GET":
        form = ArticlesModleForm()
        data = {
            'form': form,
            'article_id': article_id,
            'option': 'mod',
        }
        return render(request, 'create_article.html', data)
    # 以Post的方式来查找文章需要的json数据
    # 1.返回博客的内容数据
    instance = models.Articles.objects.filter(id=article_id).first()
    # 获取子分类的id与name
    category_row = models.Category.objects.filter(id=instance.category_id).first()
    category = []
    fcategory=0#默认父分类为没有，即0
    if category_row:#判断文章有没有选取分类
        category.append(category_row.id)
        category.append(category_row.category_name)
        fcategory=category_row.fcategory_id
    # 获取该篇文章的tag_id与tag_name
    tags_queryset = models.TagSetArticle.objects.filter(article_id=instance.id).all()
    tags = []
    if tags_queryset:#判断文章有没有设置标签
        for item in tags_queryset:
            temp = []
            temp.append(item.tag_id)
            temp.append(models.Tag.objects.filter(id=item.tag_id).first().tag_name)
            tags.append(temp)
    #判断是否设置了封面
    article_cover=''
    if(instance.article_img!=''):
        article_cover = 'media/article-cover-img/' + instance.article_img
    # 变成字典进行传输
    data = {
        'content': instance.article_content,
        'digest': instance.article_digest,
        'cover': article_cover,
        'title': instance.article_title,
        'fcategory': fcategory,
        'category': category,
        'istop': instance.article_top,
        'auth': instance.article_auth,
        'tags': tags,
        'status': 200
    }
    return JsonResponse(data)


def create_punlis(request):
    '''发表文章模态框所需要的数据'''
    # 获取父分类
    Fcatagory = models.FCategory.objects.all()
    fcatagory = []
    for obj in Fcatagory:
        tem = []
        tem.append(obj.id)
        tem.append(obj.fcategory_name)
        fcatagory.append(tem)
    # 获取子分类
    catagory = []
    status = True
    if request.POST.get('fcatagory_id'):
        id = request.POST.get('fcatagory_id')
        catagory_dict = models.Category.objects.filter(fcategory_id=id).all()
        if catagory_dict:
            for item in catagory_dict:
                tem2 = []
                tem2.append(item.id)
                tem2.append(item.category_name)
                catagory.append(tem2)
            # print(catagory)
        else:
            status = False
    # 获取父标签
    ftag_dict = models.FTag.objects.all()
    ftag = []
    for obj in ftag_dict:
        tem3 = []
        tem3.append(obj.id)
        tem3.append(obj.ftag_name)
        ftag.append(tem3)
    # print(ftag)
    # 获取子标签
    status2 = True
    tag = []
    if request.POST.get('ftag_id'):
        id = request.POST.get('ftag_id')
        id = int(id)
        tag_dict = models.Tag.objects.filter(ftag_id=id).all()
        if tag_dict:
            for obj in tag_dict:
                tem = []
                tem.append(obj.id)
                tem.append(obj.tag_name)
                tag.append(tem)
            # print(tag)
        else:
            status2 = False
    context = {
        'fcatagory': fcatagory,
        'catagory': catagory,
        'status': status,
        'ftag': ftag,
        'tag': tag,
        'status2': status2,
    }
    return JsonResponse(context)
