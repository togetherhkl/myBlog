# from django.test import TestCase
# from django.utils.decorators import method_decorator
# from django.conf import settings
#
# # Create your tests here.
# DEFAULT_CONFIG = {
#     "width": "%90",
#     "height": 360,
#     "preview_theme": "light",
#     "typewriterMode": "True",
#     "mode": "ir",
#     "debugger": "false",
#     "value": "",
#     "theme": "classic",
#     "icon": "ant",
#     "outline": "false",
# }
#
#
# class student(dict):
#     def __init__(self, config_name="default"):
#         print('init:', self)
#         self.update(DEFAULT_CONFIG)
#         print(self)
#         # self.set_configs(config_name)
#
#
# class student3:
#     def __init__(self, seq):
#         print(seq)
#
#
# class student2(student3):
#     def __init__(self, seq):
#         print('hhhh', self)
#
#
# class VditorConfig(dict):
#     def __init__(self):
#         self.update(DEFAULT_CONFIG)
#         # self.set_configs(config_name)
#
#
# from django.core.exceptions import ImproperlyConfigured
#
#
# def set_configs(self, config_name="default"):
#     configs = getattr(settings, "VDITOR_CONFIGS", None)  # 获取setting中的变量，如果没有就设置为“None”
#     if configs:
#         if isinstance(configs, dict):
#             if config_name in configs:
#                 config = configs[config_name]
#                 if not isinstance(config, dict):
#                     raise ImproperlyConfigured('VDITOR_CONFIGS["%s"] \
#                                     setting must be a dictionary type.' % config_name)
#                 self.update(config)
#             else:
#                 raise ImproperlyConfigured("No configuration named '%s' \
#                                 found in your VDITOR_CONFIGS setting." % config_name)
#         else:
#             raise ImproperlyConfigured('VDITOR_CONFIGS setting must be a\
#                             dictionary type.')
#
#
# import os
# import uuid
#
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.views.decorators.http import require_http_methods
# from .configs import VditorConfig
#
#
# VDITOR_CONFIGS = VditorConfig('default')
#
#
# @require_http_methods(['POST'])
# @method_decorator(csrf_exempt)
# def VditorImagesUploadView(request):
#     VditorImagesUpload = request.FILES.get('file[]', None)
#     VditorImagesNameList = VditorImagesUpload.name.split('.')
#     VditorImagesName = '.'.join(VditorImagesNameList)
#     VditorImagesUploadPath = os.path.join(settings.MEDIA_ROOT)
#     VditorImagesNameFull = '%s_%s' % (uuid.uuid4(), VditorImagesName)
#     if not VditorImagesNameList:
#         print('No picture')
#     else:
#         if not os.path.exists(VditorImagesUploadPath):
#             try:
#                 os.makedirs(VditorImagesUploadPath)
#             except Exception as err:
#                 print("upload failed：%s" % str(err))
#         else:
#             with open(os.path.join(VditorImagesUploadPath, VditorImagesNameFull), 'wb+') as file:
#                 for chunk in VditorImagesUpload.chunks():
#                     file.write(chunk)
#             return JsonResponse(
#                 {
#                     "msg": "Success!",
#                     "code": 0,
#                     "data": {
#                     "errFiles": [],
#                     "succMap": {
#                         VditorImagesName: os.path.join(settings.MEDIA_URL, VditorImagesNameFull),
#                         }
#                     }
#                 }
#             )