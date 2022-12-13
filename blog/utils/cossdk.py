# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。
secret_id = 'AKIDmPqEUTCeqpeKkwLZdR0KQI1cz95pNjsm'
secret_key = 'kRuEZlhQzMUO5XlpgIeprfLn24zf6HEv'
region = 'ap-chengdu'  # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
# COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None  # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


# 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
def FileUpload(file, name):
    response = client.upload_file(
        Bucket='blog-pic-1314840905',
        LocalFilePath=file,
        Key=name,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )
    print(response['ETag'])
    return response
