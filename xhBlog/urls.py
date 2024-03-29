"""xhBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# 以下三句引入是为了使用ModalFOrm上传文件到media目录进行的引入
from django.urls import path, re_path, include  # re_path为正则表达式
from django.views.static import serve
from django.conf import settings
from blog.views import home, create, upload, account, article, blogmanage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vditor/', include('vditor.urls')),
    # 寻找meida的文件，serve是django内置弄号好的，需要在setting中进行配置
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 首页
    path('home/', home.home_nav),  # 头部栏
    path('home/display/', home.home_display),  # 主页显示

    # 创作
    path('create/article/', create.create_article),  # 创作文章
    path('create/publish/', create.create_punlis),  # 获取发表模态框所需要的数据
    path('create/article/<int:nid>/mod/', create.create_article_mod),  # 修改文章内容

    # 文件上传
    path('upload/inarticle/img/', upload.upload_inatricle_img),  # 上传文章内容的图片
    path('upload/cover/img/', upload.upload_cover_img),  # 上传文章封面图

    # 登录
    path('login/', account.account_login),  # 登录
    path('login/adduser/', account.account_adduser),  # 注册用户
    path('logout/', account.account_logout),  # 注销
    path('image/code/', account.image_code),  # 获取验证码图片

    # 显示文章
    path('article/show/', article.article_show),  # 显示文章list
    path('article/gettags/', article.article_gettags),  # 获取谋篇文章的标签
    path('article/<int:nid>/show/page/', article.article_show_page),  # 展现某一篇具体的文章
    path('article/get/content/', article.article_get_content),  # 获取文章的内容
    path('article/delete/', article.article_delete),  # 删除文章

    # 博客管理
    path('blog/manage/home/', blogmanage.blogmange_home),  # 博客管理首页
    path('blog/manage/article/', blogmanage.blomanage_article),  # 博客内容管理
    path('blog/manage/article/data/', blogmanage.blomanage_article_data),  # 文章数据管理

    # Vditor的文章测试
    path('article/test/', article.article_test),
    path('article/test/getpage/', article.article_test_getpage)

]
