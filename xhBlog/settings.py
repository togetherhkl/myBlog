"""
Django settings for xhBlog project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fj@fr!u_v&3++#^)k22e6yyq)4y1(ngik!5_=-)gck!v&ulzu2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
ALLOWED_HOSTS = ['192.168.198.135', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # 注册app的名称
    'vditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.auth.AuthMiddleWare'  # 激活登录的中间件
    # 别忘记激活自己的中间件
]

ROOT_URLCONF = 'xhBlog.urls'
X_FRAME_OPTIONS = 'SAMEORIGIN'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [BASE_DIR / 'blog/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xhBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# 数据库配置
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'remote',
        'PASSWORD': 'qwer0487',
        'HOST': '192.168.198.186',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'zh-hans'  # 修改语言
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'  # 修改时候时间区域
USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False  # 不启用时区时间
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# MoalForm上传文件到media目录，添加的配置,可以在浏览器上访问文件
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"
X_FRAME_OPTIONS = 'SAMEORIGIN'

# SECURE_CONTENT_TYPE_NOSNIFF=False
# import mimetypes
# mimetypes.add_type('text/css','.less')
# mimetypes.add_type('application/javascript”','.ts')
# mimetypes.add_type('text/html','.html')
# mimetypes.add_type('application/octet-stream”','.ts')
# mimetypes.add_type('video/mp2t','.less')

"""
simpleui的配置信息
"""
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单。
    'system_keep': True,

    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。 空列表[] 为全部不显示.

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': True,
    'addmenus': [
        {
            'app': 'blog',
            'name': '个人博客管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '博客内容管理',
                    'icon': 'fa fa-user',
                    'url': 'blog/manage/article/'
                },
                {
                    'name': '博客数据分析',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                },
{
                    'name': '创作博客',
                    'icon': 'fa fa-th-list',
                    'url': 'create/article/'
                }
            ]
        },
    ]

}
