# -*cding:utf-8-*-
import hashlib
from django.conf import settings#获取配置中的secret_key

def md5(data_string):
    salt=settings.SECRET_KEY#使用配置中的随机key来作为盐值
    obj=hashlib.md5(salt.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
