from django.contrib import admin
from django.utils.html import format_html

from blog.models import Articles, Users
from vditor.fields import VditorWidget
from django.db import models
from django.urls import path
from blog.views import create
from django.urls import reverse

"""simpelui的相关配置"""
admin.site.site_header = '博客后台管理'  # 设置header
admin.site.site_title = '数据分析管理'  # 设置title
admin.site.index_title = '部分数据测试'
Users._meta.verbose_name = '用户管理'
Users._meta.verbose_name_plural = '用户管理'


class ArticlesAdmin(admin.ModelAdmin):
    labels = {
        'article_title_skip': '文章标题',
        'article_updatedate': '最近更新时间'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.labels = self.labels
    # fields = ['article_title', 'article_digest', 'user', 'article_createdate', 'category']
    list_display = ('article_title_skip', 'article_createdate', 'article_updatedate', 'category', 'user')
    # 过滤器
    list_filter = ['user', 'article_createdate']
    # 将表单分为不同的字段集进行展示
    fieldsets = [
        (None, {'fields': ['article_title', 'article_digest', 'article_content', 'category']}),
        ('时间相关', {'fields': ['article_createdate', 'article_updatedate']}),
    ]
    # 重载field
    formfield_overrides = {
        models.TextField: {'widget': VditorWidget}
    }
    # 搜索框
    search_fields = ['article_title', 'article_digest']
    search_help_text = '请输入标题和摘要进行搜索'
    # 自定义链接
    list_display_links = []


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_img', 'user_auth',)
    list_display_links = ('user_name',)


# Register your models here.
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Users, UsersAdmin)
