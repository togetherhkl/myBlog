# -*cding:utf-8-*-
from django.core import serializers  # 引入序列化器
from django.db.models import Q, Count  # 引入Q查询，也就是多条件查询,和聚合函数count
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django import forms
from django.core import validators
from django.core.validators import RegexValidator  # 引入正则表达式
from django.core.exceptions import ValidationError  # 引入错误的报错
from blog import models
from blog.utils.pagination import PagInation
from blog.utils.encrypt import md5


class UserModelForm(forms.ModelForm):
    user_phone = forms.CharField(label="手机",
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
                             # disabled=True#在编辑时不可修改
                             )
    user_email=forms.CharField(
        label='邮箱',
        validators=[validators.EmailValidator(message='请输入正确的邮箱')]
    )
    class Meta:
        model=models.Users
        fields=['user_name','user_nickname','user_sex','user_email','user_phone']
        labels={
            'user_name':'名称',
            'user_nickname':'昵称',
            'user_email':'邮箱',
            'user_phone':'手机',
            # 'user_img':'头像',
            # 'user_birth':'生日',
        }
        widgets={
            'user_name':forms.TextInput(attrs={'readOnly':'true'})
        }
def blogmange_home(request):
    '''博客管理首页'''
    if request.method=='GET':
        user_instance=models.Users.objects.filter(id=request.session['info']['id']).first()
        form=UserModelForm(instance=user_instance)
        return render(request, 'blog_manage_home.html',{'form':form})
    #修改密码
    elif request.POST.get('type'):
        data={
            'status':400,
            'old_pwd':'',
            'new_pwd':'',
            'confirm_pwd':'',
        }
        #数据校验
        old_pwd = request.POST.get('old_pwd')
        print(old_pwd)
        if old_pwd=='':
            data['old_pwd']='旧密码不能为空'
            return JsonResponse(data)
        new_pwd=request.POST.get('new_pwd')
        if new_pwd=='':
            data['new_pwd']='新密码不能为空'
            return JsonResponse(data)
        confirm_pwd=request.POST.get('confirm_pwd')
        if confirm_pwd=='':
            data['confirm_pwd']='确认密码不能为空'
            return JsonResponse(data)
        pwd=models.Users.objects.filter(id=request.session['info']['id']).values('user_pwd')
        if md5(old_pwd) != pwd[0]['user_pwd']:
            data['old_pwd'] = '输入的旧密码不正确'
            return JsonResponse(data)
        if new_pwd!=confirm_pwd:
            data['new_pwd'] = '新旧密码不一致'
            data['confirm_pwd'] = '新旧密码不一致'
            return JsonResponse(data)
        models.Users.objects.filter(id=request.session['info']['id']).update(user_pwd=md5(new_pwd))
        data['status']=200
        return JsonResponse(data)
    #完善个人信息
    else:
        user_instance=models.Users.objects.filter(id=request.session['info']['id']).first()
        form = UserModelForm(instance=user_instance,data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'blog_manage_home.html', {'form': form})
        else:
            return render(request, 'blog_manage_home.html', {'form': form})


def blomanage_article(request):
    '''内容管理首先显示的界面'''
    article_set = models.Articles.objects.filter(user_id=request.session['info']['id'],
                                                 article_status__in=[1, 2, 3]).all()  # 获取当前登录者的所有文章,不含回收站的
    article_all = article_set.count()
    article_draft = models.Articles.objects.filter(article_status=1,
                                                   user_id=request.session['info']['id']).all()  # 草稿queryset
    article_pub = models.Articles.objects.filter(article_status=2,
                                                 user_id=request.session['info']['id']).all()  # 已发表queryset
    article_audit = models.Articles.objects.filter(article_status=3,
                                                   user_id=request.session['info']['id']).all()  # 在审核queryset
    article_delete = models.Articles.objects.filter(article_status=4,
                                                    user_id=request.session['info']['id']).all()  # 回收queryset
    category_set = models.Category.objects.all()  # 这里如果还要设计个人的分类的化，需要在分类中添加user的id，这里还要进行过滤
    data = {
        'article_set': article_set,
        'article_all': article_all,
        'article_draft': article_draft.count(),  # 草稿的数量
        'article_pub': article_pub.count(),  # 已发表的数量
        'article_audit': article_audit.count(),  # 在审核的数量
        'article_delete': article_delete.count(),  # 删除的数量
        'category_set': category_set,
    }
    if request.method == "GET":
        page = request.GET.get('page')
        page_obj = PagInation(article_set, 6, page, 3)
        data['article_set'] = page_obj.queryset
        data['page'] = page_obj.page
        data['show_start_page'] = page_obj.show_start_page
        data['show_end_page'] = page_obj.show_end_page
        data['page_count'] = page_obj.page_count
        return render(request, 'blog_manage_article.html', data)
    if request.method == "POST":
        # 1.接受前端传过来的文章状态的查询类型
        article_status = request.POST.get('search_op', '2')  # 默认为2，以发表的状态
        page = request.POST.get('page', 1)
        # 1.1检验数据是否合理
        if article_status.isdecimal():
            article_status = int(article_status)
        else:
            article_status = 2
        if article_status == 0:  # 返回所有的文章
            data = SetArticleData(article_set, page, data)
            return JsonResponse(data)
        elif article_status == 1:  # 返回草稿状态的文章
            data = SetArticleData(article_draft, page, data)
            return JsonResponse(data)
        elif article_status == 2:  # 返回发表状态的文章
            data = SetArticleData(article_pub, page, data)
            return JsonResponse(data)
        elif article_status == 3:  # 返回审核状态的文章
            data = SetArticleData(article_audit, page, data)
            return JsonResponse(data)
        elif article_status == 4:  # 返回回收状态的文章
            data = SetArticleData(article_delete, page, data)
            return JsonResponse(data)
        elif article_status == 5:  # 返回分类+搜索内容的模糊查询结果（标题与摘要）
            search_text = request.POST.get('search_text')
            category_id = request.POST.get('category_id')
            # 1.检验id是否合理
            if category_id.isdecimal():
                category_id = int(category_id)
            else:
                category_id = 0
            # 2.操作数据库进行模糊查询
            if category_id == 0:
                article_queryset = models.Articles.objects.filter(
                    Q(article_title__contains=search_text) | Q(article_digest__contains=search_text),
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

    return JsonResponse({'status': 'no'})


def SetArticleData(article_set, page, data):
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


def blomanage_article_data(request):
    '''
    文章数据分析
    '''
    if request.method == "GET":
        return render(request, 'manage_articles_data.html')
    else:
        data_type = request.POST.get('data_type')
        # 获取分类的id和name
        # xAxis_data = list(models.Category.objects.values_list('id','category_name', flat=True))
        xAxis = list(
            models.Category.objects.filter(user_id=request.session['info']['id']).values('id', 'category_name'))
        # print(xAxis)
        # 聚合查询，查询出对应分类的文章数目
        temp = models.Articles.objects.filter(user_id=request.session['info']['id']).values('category_id').annotate(
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

        # 构造柱状图前端数据
        if data_type == 'barchar':
            data = {
                'msg': 'yes',
            }
            for x in xAxis:
                series_data.append(x['total'])
            #添加未分类数据
            xAxis_data.append(temp2[0])
            series_data.append(temp2[1])
            data['xAxis_data']=xAxis_data
            data['series_data'] = series_data
            return JsonResponse(data)
        #构造饼图
        if data_type == 'handchar':
            data={
                'msg':'success',
            }
            for x in xAxis:
                temp_dict={}
                temp_dict['value']=x['total']
                temp_dict['name']=x['category_name']
                series_data.append(temp_dict)
            data['series_data']=series_data
            return JsonResponse(data)
        return render(request, 'manage_articles_data.html')
