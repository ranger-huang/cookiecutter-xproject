# coding=utf-8
from urllib.parse import urlparse, urljoin

import six
from aliyun_oss2_storage.backends import AliyunBaseStorage as _AliyunBaseStorage
from django.conf import settings
from django.utils.encoding import force_str


class AliyunBaseStorage(_AliyunBaseStorage):
    """
    Aliyun OSS2 Storage
    """

    def __init__(self, config_prefix='ALIYUN', **kwargs):
        self.conf_prefix = config_prefix.upper()
        super().__init__()

    def _get_config(self, name):
        if not name.startswith(self.conf_prefix):
            name = "_".join([self.conf_prefix, name])
        return super()._get_config(name)

    def _create_bucket(self, auth):
        bucket = self._get_bucket(auth)
        bucket.create_bucket(self._get_config('BUCKET_ACL_TYPE'))
        return bucket

    def _check_bucket_acl(self, bucket):
        if bucket.get_bucket_acl().acl != self._get_config('BUCKET_ACL_TYPE'):
            bucket.put_bucket_acl(self._get_config('BUCKET_ACL_TYPE'))
        return bucket

    def url(self, name):
        name = self._normalize_name(self._clean_name(name))
        # name = filepath_to_uri(name) # 这段会导致二次encode
        name = name.encode('utf8')
        # 做这个转化，是因为下面的_make_url会用urllib.quote转码，转码不支持unicode，会报错，在python2环境下。
        if name.startswith(self.location.encode('utf8')):
            return force_str(name)
        return self.bucket._make_url(self.bucket_name, name)

    def _get_target_name(self, name):
        # fix name转换到云存储的相对路径
        p = urlparse(urljoin(self.location, self._clean_name(name)))
        name = p.path
        name = name.lstrip("/")
        if six.PY2:
            name = name.encode('utf-8')
        return name

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


class AliyunMediaStorage(AliyunBaseStorage):
    location = settings.MEDIA_URL


class AliyunStaticStorage(AliyunBaseStorage):
    location = settings.STATIC_URL
