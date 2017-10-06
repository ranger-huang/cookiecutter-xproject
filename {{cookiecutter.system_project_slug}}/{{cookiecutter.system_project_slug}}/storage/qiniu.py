# -*- coding: utf-8 -*-
from {{cookiecutter.system_slug}}_conf import constants

"""
    文件存储器
    主要使用云存储服务，覆盖默认配置，以同名文件覆盖方式来保持文件，而非重命名上传，
    重写Storage.get_available_name以达到同名文件覆盖
"""


from qiniustorage.backends import QiniuStorage, QiniuFile


class XZQiniuStorage(QiniuStorage):
    def __init__(
            self,
            access_key=constants.QINIU_ACCESS_KEY,
            secret_key=constants.QINIU_SECRET_KEY,
            bucket_name=constants.QINIU_BUCKET_NAME,
            bucket_domain=constants.QINIU_BUCKET_DOMAIN,
            secure_url=constants.QINIU_SECURE_URL):
        super().__init__(access_key=access_key, secret_key=secret_key,
                         bucket_name=bucket_name, bucket_domain=bucket_domain,
                         secure_url=secure_url)

    def _open(self, name, mode='rb'):
        return XZQiniuFile(name, self, mode)

    def get_available_name(self, name, max_length=None):
        # qiniu 针对一个uri 不允许覆盖上传
        # 所以在这里检查后删除云端文件再上传覆盖
        if self.exists(name):
            try:
                self.delete(name)
            except:
                pass
        return name

    def thumbnail_url(self, name, version, step='?'):
        if self.secure_url:
            return '%s://%s%s%s%s' % (
                'https', self.secure_url, self._clean_name(name), step, version)
        return '%s://%s%s%s%s' % (
            'http', self.bucket_domain, self._clean_name(name), step, version)


class XZQiniuFile(QiniuFile):
    def thumbnail_url(self, version=None):
        return self._storage.thumbnail_url(self.name, version=version)



class StaticXZQiniuStorage(XZQiniuStorage):
    location = 'static'


class MediaXZQiniuStorage(XZQiniuStorage):
    location = 'media'
