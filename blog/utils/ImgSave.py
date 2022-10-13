# -*cding:utf-8-*-
from datetime import datetime
import os
import random
def ImgSave(img,path):
    '''
    img:传入一张图片
    path:图片要上传的文件路径
    返回重命名的图片的名字，和上传后图片所在的路径
    '''
    #获取图片的后缀
    suffix = img.name.split('.')[1]
    # 时间+3位随机数命名
    img.name = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999)) + '.' + suffix
    file_path=os.path.join(path,img.name)
    # print(media_path)
    # 把图片写入路径当中
    f = open(file_path, 'wb')
    for chunk in img.chunks():
        f.write(chunk)
    f.close()
    return img.name,file_path

def ImgDel(path):
    '''传入需要删除的图片的路径'''
    os.remove(path)