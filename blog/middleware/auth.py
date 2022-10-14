# -*cding:utf-8-*-
from django.utils.deprecation import MiddlewareMixin#引入中间件
from django.shortcuts import HttpResponse,redirect

class AuthMiddleWare(MiddlewareMixin):#判断用户是否登录
    def process_request(self,request):
        #如果没有返回值，则返回None，继续往后走
        #如果有返回值，则根据返回的值进行返回
        # return HttpResponse('无权')#如果有这个返回值，那么中间件就不会继续往后面继续走了，直接返回
        #排除不需要登录就可以访问的界面
        #request.path_info获取当前用户请求的URL
        if request.path_info in ['/login/','/image/code/','/home/display/','/home/']:
            return
        #读取session，如果对方已经登录，则会读取到sesson的值，就可以往后走了
        session=request.session.get('info')
        if session:
            return
        else:#没有登录,返回到登录界面
            return redirect('/login/')
    def process_response(self,request,response):
        # print('M1走了')
        return response
