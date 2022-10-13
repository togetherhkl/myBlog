# -*cding:utf-8-*-
import time

from django.shortcuts import render,HttpResponse,redirect
from django import forms
from blog import models
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone#引入时间
from blog.utils.checkcode import CreateVerifyImg#验证码生成图片
from django.core.exceptions import ValidationError#引入错误提示
from blog.utils.encrypt import md5#md5的加密
class LoginForm(forms.Form):
    '''登录界面的表单'''
    username=forms.CharField(
        label='用户名',
        required=True,
        error_messages={#更改错误信息
          'required':'需要填入信息',
        },
        widget=forms.TextInput(attrs={'type':'text','class':'username','placeholder':'用户名'}),

    )
    password=forms.CharField(
        label='密码',
        required=True,
        widget=forms.PasswordInput(attrs={'class':'password','placeholder':'密码'},render_value=True)
        #render_value=True错误的信息不会被删除
    )
    #验证码
    verifycode=forms.CharField(
        label='验证码',
        required=True,
        widget=forms.TextInput(attrs={'type':'text','name':'img-code','placeholder':'请输入验证码'},)
    )
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)

class UserModelForm(forms.ModelForm):
    '''注册界面的表单'''
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.TextInput(attrs={'type': 'password', }))
    class Meta:
        model=models.Users
        fields=['user_name','user_pwd','confirm_password']
        widgets={
            'user_pwd':forms.TextInput(attrs={'type':'password'})
        }
        labels={
            'user_name':'用户名',
            'user_pwd':'密码'
        }
    def clean_user_pwd(self):
        '''密码的钩子方法'''
        pwd=self.cleaned_data.get('user_pwd')
        return md5(pwd)
    def clean_confirm_password(self):
        '''确认密码的钩子方法'''
        pwd = self.cleaned_data.get('user_pwd')
        confirm_pwd = self.cleaned_data.get('confirm_password')
        if md5(confirm_pwd) != pwd:
            raise ValidationError('输入的密码不一致')#提示错误
        return md5(confirm_pwd)

def account_login(request):
    '''登录功能'''
    if request.method=="GET":#如果是get请求
        form=LoginForm()
        formset=UserModelForm()
        context={
            'form':form,
            'formset':formset,
        }
        print(context)
        return render(request, 'login.html',context)
    # 如果是POST请求
    form=LoginForm(data=request.POST)
    formset = UserModelForm()
    context = {
        'form': form,
        'formset': formset,
    }
    if form.is_valid():#输入的为有效数据
        #把imagecode从form.cleaned_data中取出并去除
        verifycode=form.cleaned_data.pop('verifycode')
        if not verifycode:
            return render(request, 'login.html', context)
        #与session中的verifycode做对比（转化为小写）
        if verifycode.lower()!=request.session.get('verifycode').lower():
            form.add_error('verifycode','验证码错误')
            return render(request,'login.html',context)

        # row_obj=models.Users.objects.filter(**form.cleaned_data).first()
        row_obj=models.Users.objects.filter(user_name=form.cleaned_data.get('username'),user_pwd=form.cleaned_data.get('password')).first()
        if not row_obj:
            form.add_error('password','账号或者密码输入错误')
            #提交错误的信息，别忘了在前端页面当中加入错误信息的引入{{form.usernaem.errors.0}}
            return render(request,'login.html',context)
        #验证正确，添加seesion
        request.session['info']={'id':row_obj.id,'name':row_obj.user_name}
        #设置session的有效时间,7天的有效时间
        request.session.set_expiry(60*60*24*7)
        #防止验证码复用，删除验证码
        request.session.delete('verifycode')
        return redirect('/home/display/')
    return render(request,'home_display.html',context)


def account_logout(request):
    '''退出'''
    request.session.clear()
    return redirect('/login/')

def image_code(request):
    '''请求验证码'''
    verifycode,img=CreateVerifyImg(120,60)
    #把验证码写入到session进行验证，在登录的时候做验证
    request.session['verifycode']=verifycode
    #设置session的超时时间60s
    request.session.set_expiry(60)
    return HttpResponse(img)

def account_adduser(request):
    '''注册用户'''
    # print(request.POST)
    form=UserModelForm(data=request.POST)
    data={}
    if form.is_valid():
        # print(form.cleaned_data)#输出数据进行查看

        # print(form.cleaned_data['user_name'])
        models.Users.objects.create(
            user_name=form.cleaned_data['user_name'],
            user_pwd=form.cleaned_data['user_pwd'],
            )
        data['status']=200
        data['msg']='注册成功'

    else:
        # print(form.errors)
        data['msg']=form.errors#收集错误消息
        data['status']=404
    return JsonResponse(data)
