# -*cding:utf-8-*-
from django.shortcuts import HttpResponse
from django.http import JsonResponse
import os
from datetime import datetime
import random


def upload_inatricle_img(request):
    '''上传文章中所使用的图片'''
    # print(request.FILES)#测试文件类型
    #获取文件的上传列表
    file_list = request.FILES.getlist('file[]')
    print(len(file_list))
    #判断文件是否为空
    if not file_list:
        res={
            'code':404,
            'msg':'无上传文件',
        }
        return JsonResponse(res)
    name=[]
    path=[]
    for file_obj in file_list:
        # print(i.name)
        # name=i.name
        # 重命名文件防止文件重复
        #获取图图片的后缀
        suffix=file_obj.name.split('.')[1]
        #时间+3位随机数命名
        file_obj.name=datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(100,999))+'.'+suffix
        # print(file_obj.name)
        name.append(file_obj.name)
        file_path = os.path.join('media', 'article-inner-img', file_obj.name)
        path.append(file_path)
        # print(media_path)
        #把图片写入路径当中
        f = open(file_path, 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
    res = {
        "msg": "上传成功",
        "code": 200,
        "data": {
            'name':name,
            'url':path,
            'count':len(file_list),
        }
    }
    return JsonResponse(res)
