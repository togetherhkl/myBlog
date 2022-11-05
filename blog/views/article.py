# -*cding:utf-8-*-
import json

from django.db.models import Q
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from blog import models

from blog.utils.pagination import PagInation  # 引入自己写的分页插件


def article_show(request):
    '''返回某个分类下所有文章的文章信息'''
    if request.method == "GET":
        # print(request.GET)
        category = request.GET.get('category_id')
        if category:
            category = int(category)
            queryset = models.Articles.objects.filter(category_id=category, user_id=1,article_auth=1).all().order_by('-article_updatedate')
            # 默认只显示xh这个用户的,并且是允许分享的文章
            page = request.GET.get('page')
            page_obj = PagInation(queryset, 5, page, 2)
            data = {
                'objs': page_obj.queryset,
                'page': page_obj.page,
                'show_start_page': page_obj.show_start_page,
                'show_end_page': page_obj.show_end_page,
                'page_count': page_obj.page_count,
            }

            return render(request, 'articles_show.html', data)
        else:
            search_text = request.GET.get('search_text')
            queryset = models.Articles.objects.filter(
                Q(article_title__contains=search_text)|Q(article_digest__contains=search_text),
                user_id=1,
            ).all()  # 默认只显示xh这个用户的,标题和摘要的模糊搜索
            page = request.GET.get('page')
            page_obj = PagInation(queryset, 5, page, 2)
            data = {
                'objs': page_obj.queryset,
                'page': page_obj.page,
                'show_start_page': page_obj.show_start_page,
                'show_end_page': page_obj.show_end_page,
                'page_count': page_obj.page_count,
            }
            return render(request, 'articles_show.html', data)
    if request.method=="POST":
        if request.POST.get('type')=='add_comment':
            data={}
            #判断用户是否登录
            if request.session['info']==None:
                data['status']=400
                data['msg']='请先登录'
                return JsonResponse(data)
            article_id=request.POST.get('article_id')
            comment=request.POST.get('comment')
            #插入数据库
            models.Comments.objects.create(
                article_id=article_id,
                user_id=request.session['info']['id'],
                comment_content=comment
            )
            data['status']=200
            data['msg']='评论发表成功'
            return JsonResponse(data)
        if request.POST.get('type') == 'get_comment':
            #获取相关的评论信息
            data={'msg':'yyyy'}
            article_id = request.POST.get('article_id')
            instance=models.Comments.objects.filter(
                article_id=article_id
            ).values('comment_content','user__user_name','comment_createdate')
            #把列表转化为json数据
            data['values']=list(instance)
            return JsonResponse(data)
        if request.POST.get('type') == 'article_detail':
            #获取文章的相关信息
            data={'msg':'yes'}
            article_id = request.POST.get('article_id')
            instance=models.Articles.objects.filter(
                user_id=1,
                id=article_id,
            ).values('article_title','user__user_name','article_createdate','article_updatedate')
            #获取相关标签
            tags=models.TagSetArticle.objects.filter(article_id=article_id).values(
                'tag_id','tag__tag_name'
            )
            data['article_detail']=list(instance)
            data['tags']=list(tags)
            return JsonResponse(data)
        return HttpResponse('请求错误')


def article_gettags(request):
    '''获取某篇文章的所有标签'''
    article_id = request.POST.get('article_id')
    article_id = int(article_id)
    quryset = models.TagSetArticle.objects.filter(article_id=article_id).all()
    tags = []
    status = 400
    for item in quryset:
        tag_id = item.tag_id
        tag_name = models.Tag.objects.filter(id=tag_id).first().tag_name
        tags.append(tag_name)
        status = 200
    # print(tags)
    data = {
        'tags': tags,
        'status': status
    }
    return JsonResponse(data)


def article_show_page(request, nid):
    '''返回文章的html代码共前端解析'''
    # bug思考，这里会导致越权访问，如果用户不止一个，他在这上面发表了文章，但是他又不想给别人看。
    # 这里通过修改前端get中的数字就可以越权访问到别人的文章
    article_id = nid
    obj = models.Articles.objects.filter(id=article_id,user_id=1,article_auth=1).first()
    #值运行查看xh并且分享的文章
    if not obj:
        status = 400
        msg = "文章不存在"
        # page=''
    else:
        status = 200
        # page=obj.article_content
        msg = ''
    data = {
        # 'page':page,
        'status': status,
        'msg': msg,
        'article_id': article_id,
    }
    return render(request, 'article_show_page.html', data)


def article_get_content(request):
    '''获取博客文章的具体内容'''
    article_id = request.POST.get('page_id')
    article_id = int(article_id)
    obj = models.Articles.objects.filter(id=article_id).first()
    page = obj.article_content
    # print(page)
    data = {
        'page': page,
        'msg': 'success',
    }
    return JsonResponse(data)


def article_delete(request):
    '''删除文章'''
    # 定义返回前端的数据
    data = {}
    # 1.接受前端传过来的文章nid
    nid = request.POST.get('id')
    op_del = request.POST.get('op_del')
    # print(op_del)
    ## 1.1验证nid是不是作者的文章，以免别人修改nid来删除别人的文章
    queryset = models.Articles.objects.filter(id=nid, user_id=request.session['info']['id'])
    if not queryset:
        # 1.2验证失败
        data['status'] = 404
        data['msg'] = '删除错误'
    else:
        # 2.验证成功，操纵数据库
        if op_del == 'recycle':
            models.Articles.objects.filter(id=nid, user_id=request.session['info']['id']).update(article_status=4)
            data['status'] = 200
            data['msg'] = '删除成功，文章已经被放入回收箱'
        elif op_del == 'del_complete':
            models.Articles.objects.filter(id=nid, user_id=request.session['info']['id']).delete()
            data['status'] = 200
            data['msg'] = '文章已删除'
        else:
            data['status'] = 404
            data['msg'] = '删除错误'
    # 3.返回前端需要的数据
    return JsonResponse(data)


# 下面是测试的例子
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin


@xframe_options_sameorigin
def article_test(request):
    obj = models.Articles.objects.filter(id=15).first()
    page = obj.article_content
    # print(page)
    return render(request, 'test.html', {'page': page})


@xframe_options_sameorigin
def article_test_getpage(request):
    obj = models.Articles.objects.filter(id=11).first()
    page = obj.article_content
    # print(page)
    data = {
        'page': page,
        'msg': 'success',
    }
    return JsonResponse(data)
