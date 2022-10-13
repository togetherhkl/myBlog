# -*cding:utf-8-*-
import random
from captcha.image import ImageCaptcha

def RandonCodeText(num):
    '''
    生成验证函数，num为返回的验证码位数
    '''
    text_list=[]
    for i in range(10):#1-9
        text_list.append(str(i))
    for i in range(65,91):#A-Z
        text_list.append(chr(i))
    for i in range(97,123):#a-z
        text_list.append(chr(i))
    example=random.sample(text_list,num)#多用于截取列表的指定长度的随机数，但是不会改变列表本身的排序
    # print(example)
    verify_code=''.join(example)
    # print(verify_code)
    return verify_code

def CreateVerifyImg(width=160,height=40):
    '''
    生成图片验证码图片，返回验证码字符与内存中的图片
    width:图片长度
    height:图片的宽度
    '''
    width=int(width)
    height=int(height)
    img=ImageCaptcha(width=width,height=height)
    verify_code=RandonCodeText(4)#获取四位数的验证码
    verify_code=''.join(verify_code)#确保安全再次转化为字符串
    # img.generate_image(verify_code)#生成图片
    verify_img=img.generate(verify_code)#写进内存中的图片
    # img.write(verify_code,'image2/'+verify_code+'.jpg' )#保存图片，图片名即为里面的数字
    # return verify_code,img.generate_image(verify_code)
    return verify_code,verify_img.getvalue()
# CreateVerifyImg()