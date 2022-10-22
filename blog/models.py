from django.db import models
from django.utils import timezone

# Create your models here.
class FTag(models.Model):
    '''父标签类'''
    ftag_name=models.CharField(verbose_name='父标签名称',max_length=50)
    ftag_description=models.TextField(verbose_name='父标签描述')
    ftag_createdate=models.DateTimeField(verbose_name='创建时间')

class Tag(models.Model):
    '''标签类'''
    tag_name=models.CharField(verbose_name='标签名称',max_length=50)
    tag_description=models.TextField(verbose_name='标签描述')
    tag_createdate=models.DateTimeField(verbose_name='创建时间')
    #级联删除
    ftag=models.ForeignKey(verbose_name='父标签',to='FTag',to_field='id',on_delete=models.CASCADE)
    def __str__(self):
        return self.tag_name

class FCategory(models.Model):
    '''父分类表'''
    fcategory_name=models.CharField(verbose_name='父分类名称',max_length=50)
    fcategory_description=models.TextField(verbose_name='父标签描述')
    fcategory_createdate=models.DateTimeField(verbose_name='创建时间')

class Category(models.Model):
    '''分类类'''
    category_name=models.CharField(verbose_name='分类名称',max_length=50)
    category_description=models.TextField(verbose_name='分类描述')
    category_createdate=models.DateTimeField(verbose_name='创建时间')
    fcategory=models.ForeignKey(verbose_name='父分类',to='FCategory',to_field='id',on_delete=models.CASCADE)
    jumpaddress=models.CharField(verbose_name='跳转地址',max_length=128,default="#")
    def __str__(self):
        return self.category_name

class Users(models.Model):
    '''用户类'''
    user_name=models.CharField(verbose_name='用户名',max_length=20,unique=True)
    user_nickname=models.CharField(verbose_name='用户昵称',max_length=20,null=True,blank=True)
    sex_choices=(
        (1,'男'),
        (2,'女'),
    )
    user_sex=models.SmallIntegerField(verbose_name='性别',choices=sex_choices,default=1)
    user_email=models.CharField(verbose_name='用户邮箱',max_length=32,null=True,blank=True)
    user_phone=models.CharField(verbose_name='用户手机',max_length=11,null=True,blank=True,unique=True)
    user_pwd=models.CharField(verbose_name='用户密码',max_length=128)
    user_img=models.FileField(verbose_name='用户头像',upload_to='usersimg/',max_length=128,default='media/user_avatar/default_avatar.png')
    user_createdate=models.DateTimeField(verbose_name='注册时间',default=timezone.now())
    user_birth=models.DateField(verbose_name='出生日期',null=True,blank=True)
    auth_choices=(
        (1,'普通权限'),
        (2,'管理员权限'),
        (3,'使用权限'),
    )
    user_auth=models.SmallIntegerField(verbose_name='用户权限',choices=auth_choices,default=1)
    level_choices=(
        (1,'普通'),
        (2,'VIP'),
        (3,'超级VIP'),
    )
    user_level=models.SmallIntegerField(verbose_name='用户等级',choices=level_choices,default=1)
    def __str__(self):
        return self.user_name

class Articles(models.Model):
    '''博文类'''
    article_title=models.CharField(verbose_name='博文标题',max_length=32)
    article_digest=models.CharField(verbose_name='博文摘要',max_length=400)
    article_content=models.TextField(verbose_name='博文内容')
    #作者账户被删除，那么他的文章也会被删除
    user=models.ForeignKey(verbose_name='发表用户',to='Users',to_field='id',on_delete=models.CASCADE)
    article_createdate=models.DateTimeField(verbose_name='发表日期',default=timezone.now())
    article_updatedate=models.DateTimeField(verbose_name='更新日期')
    #如果分类别删除，博文的分类置空
    category=models.ForeignKey(verbose_name='博文分类',to='Category',to_field='id',null=True,blank=True,on_delete=models.SET_NULL)
    # tag=models.ForeignKey(verbose_name='标签',to='Tag',to_field='id',null=True,blank=True,on_delete=models.SET_NULL)
    top_choices=(
        (0,'不置顶'),
        (1,'置顶')
    )
    article_top=models.SmallIntegerField(verbose_name='是否置顶',choices=top_choices,default=0)
    status_choices=(
        (1,'草稿'),
        (2,'已发表'),
        (3,'审核中')
    )
    article_status=models.SmallIntegerField(verbose_name='发表状态',choices=status_choices,default=3)
    article_img=models.CharField(verbose_name='文章贴图',null=True,blank=True,max_length=100)
    article_view=models.BigIntegerField(verbose_name='浏览量',default=0)
    article_like=models.BigIntegerField(verbose_name='点赞量',default=0)
    article_comment=models.BigIntegerField(verbose_name='评论数',default=0)
    article_collect=models.BigIntegerField(verbose_name='收藏量',default=0)
    auth_choices=(
        (0,'不共享'),
        (1,'共享'),
    )
    article_auth=models.SmallIntegerField(verbose_name='共享权限',choices=auth_choices,default=1)

class TagSetArticle(models.Model):
    '''标签设置博文类'''
    #如果删除标签则标签置空
    tag=models.ForeignKey(verbose_name='标签名',to='Tag',to_field='id',null=True,blank=True,on_delete=models.SET_NULL)
    #如果博文被删除，则相应的记录也删除
    article=models.ForeignKey(verbose_name='博文名',to='Articles',to_field='id',on_delete=models.CASCADE)

class Comments(models.Model):
    '''评论类'''
    article=models.ForeignKey(verbose_name='评论的文章',to='Articles',to_field='id',on_delete=models.CASCADE)
    user=models.ForeignKey(verbose_name='评论者',to='Users',to_field='id',on_delete=models.CASCADE)
    comment_content=models.TextField(verbose_name='评论内容')
    comment_like=models.BigIntegerField(verbose_name='点赞数')
    #父评论关联自己的评论id
    comment_fid=models.ForeignKey(verbose_name='父评论',to='Comments',to_field='id',on_delete=models.CASCADE)
    comment_createdate=models.DateTimeField(verbose_name='创建时间')

class FriendsLink(models.Model):
    '''友链类'''
    friendslink_links=models.CharField(verbose_name='友链链接',max_length=255)
    friendslink_name=models.CharField(verbose_name='友链名称',max_length=32)
    friendslink_description=models.TextField(verbose_name='友链描述')
    friendslink_logo=models.FileField(verbose_name='友链Logo',null=True,blank=True,upload_to='linkimg/')
