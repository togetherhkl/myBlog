# -*cding:utf-8-*-
from django.core import serializers#引入序列化器
from django.db.models import Q
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from blog import models
from blog.utils.pagination import PagInation
def blogmange_home(request):
    '''博客管理首页'''
    return render(request,'blog_manage_home.html')

def blomanage_article(request):
    '''内容管理首先显示的界面'''
    article_set=models.Articles.objects.filter(user_id=request.session['info']['id'],article_status__in=[1,2,3]).all()#获取当前登录者的所有文章,不含回收站的
    article_all=article_set.count()
    article_draft=models.Articles.objects.filter(article_status=1,user_id=request.session['info']['id']).all()#草稿queryset
    article_pub=models.Articles.objects.filter(article_status=2,user_id=request.session['info']['id']).all()#已发表queryset
    article_audit=models.Articles.objects.filter(article_status=3,user_id=request.session['info']['id']).all()#在审核queryset
    article_delete=models.Articles.objects.filter(article_status=4,user_id=request.session['info']['id']).all()#回收queryset
    category_set=models.Category.objects.all()#这里如果还要设计个人的分类的化，需要在分类中添加user的id，这里还要进行过滤
    data = {
        'article_set': article_set,
        'article_all': article_all,
        'article_draft': article_draft.count(),  # 草稿的数量
        'article_pub': article_pub.count(),  # 已发表的数量
        'article_audit': article_audit.count(),  # 在审核的数量
        'article_delete': article_delete.count(),  # 删除的数量
        'category_set': category_set,
    }
    if request.method=="GET":
        page=request.GET.get('page')
        page_obj=PagInation(article_set,6,page,3)
        data['article_set']=page_obj.queryset
        data['page']= page_obj.page
        data['show_start_page']= page_obj.show_start_page
        data['show_end_page']= page_obj.show_end_page
        data['page_count']=page_obj.page_count
        return render(request,'blog_manage_article.html',data)
    if request.method=="POST":
        #1.接受前端传过来的文章状态的查询类型
        article_status=request.POST.get('search_op','2')#默认为2，以发表的状态
        page=request.POST.get('page',1)
        #1.1检验数据是否合理
        if article_status.isdecimal():
            article_status=int(article_status)
        else:
            article_status=2
        if article_status==0:#返回所有的文章
            data = SetArticleData(article_set, page, data)
            return JsonResponse(data)
        elif article_status==1:#返回草稿状态的文章
            data = SetArticleData(article_draft, page, data)
            return JsonResponse(data)
        elif article_status == 2:  # 返回发表状态的文章
            data = SetArticleData(article_pub, page, data)
            return JsonResponse(data)
        elif article_status==3:#返回审核状态的文章
            data=SetArticleData(article_audit,page,data)
            return JsonResponse(data)
        elif article_status==4:#返回回收状态的文章
            data = SetArticleData(article_delete, page, data)
            return JsonResponse(data)
        elif article_status == 5:  # 返回分类+搜索内容的模糊查询结果（标题与摘要）
            search_text=request.POST.get('search_text')
            category_id=request.POST.get('category_id')
            #1.检验id是否合理
            if category_id.isdecimal():
                category_id = int(category_id)
            else:
                category_id = 0
            #2.操作数据库进行模糊查询
            if category_id==0:
                article_queryset=models.Articles.objects.filter(
                    Q(article_title__contains=search_text)|Q(article_digest__contains=search_text),
                    user_id=request.session['info']['id'],
                ).all()
            else:
                article_queryset = models.Articles.objects.filter(
                    Q(article_title__contains=search_text) | Q(article_digest__contains=search_text),
                    user_id=request.session['info']['id'],
                    category_id=category_id,
                ).all()
            data = SetArticleData(article_queryset, page, data)
            return JsonResponse(data)

    return JsonResponse({'status':'no'})

def SetArticleData(article_set,page,data):
    '''
    设置前端博客内容管理时，所需要的数据
    article_set:查询后的结果
    page:第几个分页
    data:返回前端的数据
    '''
    page_obj = PagInation(article_set, 6, page, 3)
    data['article_set'] = serializers.serialize('json', page_obj.queryset)
    # 设置分页信息
    data['page'] = page_obj.page
    data['show_start_page'] = page_obj.show_start_page
    data['show_end_page'] = page_obj.show_end_page
    data['page_count'] = page_obj.page_count
    data['category_set'] = 0
    return data
