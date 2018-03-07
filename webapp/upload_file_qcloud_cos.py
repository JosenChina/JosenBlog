# _*_ coding: utf-8 _*_
# filename: upload_file_qcloud_cos.py
# 腾讯云对象存储
# -*- coding=utf-8
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

# 腾讯云COSV5Python SDK, 目前可以支持Python2.6与Python2.7

# pip安装指南:pip install -U cos-python-sdk-v5

# cos最新可用地域,参照https://www.qcloud.com/document/product/436/6224

# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
secret_id = os.environ.get('cos_secret_id')    # 替换为用户的secret_id
secret_key = os.environ.get('cos_secret_key')     # 替换为用户的secret_key
region = os.environ.get('cos_region')    # 替换为用户的region
token = ''                 # 使用临时秘钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)


class cos_class:
    cos_path = os.environ.get('cos_path') or 'http://%s-%s.cosgz.myqcloud.com' % (os.environ.get('cos_bucket'), os.environ.get('cos_app_id'))

    @staticmethod
    def upload_file(file_body, file_name):
        # 文件流 简单上传
        response = client.put_object(
            Bucket=os.environ.get('cos_bucket')+'-'+os.environ.get('cos_app_id'),  # Bucket由bucketname-appid组成
            Body=file_body,
            Key=file_name,
            # StorageClass='STANDARD',
            # CacheControl='no-cache',
            # ContentDisposition='download.txt'
            )
        print response['ETag']

    @staticmethod
    def upload_str(_bytes, file_name):
        # 字节流 简单上传
        response = client.put_object(
            Bucket=os.environ.get('cos_bucket')+'-'+os.environ.get('cos_app_id'),
            Body=_bytes,
            Key=file_name,
            # CacheControl='no-cache',
            # ContentDisposition='download.txt'
        )
        print response['ETag']

    @staticmethod
    def download_file(file_name, output_path):
        # 文件下载 获取文件到本地
        try:
            response = client.get_object(
                Bucket=os.environ.get('cos_bucket')+'-'+os.environ.get('cos_app_id'),
                Key=file_name,
            )
            response['Body'].get_stream_to_file(output_path)
        except CosServiceError as e:
            print e.get_origin_msg()
            print e.get_digest_msg()
            print e.get_status_code()
            print e.get_error_code()
            print e.get_error_msg()
            print e.get_resource_location()
            print e.get_trace_id()
            print e.get_request_id()

    @staticmethod
    def download_str(file_name):
            # 文件下载 获取文件流
        try:
            response = client.get_object(
                Bucket=os.environ.get('cos_bucket')+'-'+os.environ.get('cos_app_id'),
                Key=file_name,
            )
            fp = response['Body'].get_raw_stream()
            print fp.read(2)
        except CosServiceError as e:
            print e.get_origin_msg()
            print e.get_digest_msg()
            print e.get_status_code()
            print e.get_error_code()
            print e.get_error_msg()
            print e.get_resource_location()
            print e.get_trace_id()
            print e.get_request_id()

    @staticmethod
    def delete_file(file_name):
        response = client.delete_object(
            os.environ.get('cos_bucket') + '-' + os.environ.get('cos_app_id'),
            Key=file_name
        )


