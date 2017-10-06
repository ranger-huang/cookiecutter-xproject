# -*- coding: utf-8 -*-
import mimetypes
from upyun import UpYun
from upyun_django.storage.storage import UpYunStorage, UpYunStorageFile
from upyun_django.storage.utils import setting
from {{cookiecutter.system_slug}}_conf import constants

"""
    文件存储器
    主要使用云存储服务，覆盖默认配置，以同名文件覆盖方式来保持文件，而非重命名上传，
    重写Storage.get_available_name以达到同名文件覆盖
"""


class XZUpyunStorage(UpYunStorage):

    def __init__(self, username=None, password=None, bucket=None, domain=None,
                 **kwargs):
        username = username or constants.WORKOUT_UPYUN_ACCOUNT
        password = password or constants.WORKOUT_UPYUN_PASSWORD
        bucket = bucket or constants.WORKOUT_UPYUN_BUCKET
        domain = domain or constants.WORKOUT_UPYUN_DOMAIN
        self.debug = kwargs.get('debug', False)
        super().__init__(username=username, password=password, bucket=bucket,
                         domain=domain, **kwargs)
        self._root = ''

    @property
    def api(self):
        if self._api is None:
            self._api = UpYun(
                self._bucket,
                username=self._username,
                password=self._password,
                debug=self.debug,
                timeout=self._timeout,
                endpoint=self._endpoint
            )
        return self._api

    def _get_or_create_folder(self):
        return dict()

    def _save(self, name, content):
        clean_name = self._clean_name(name)
        content_type = getattr(content, 'content_type',
                               mimetypes.guess_type(name)[0] or 'text/plain')
        headers = {
            'Mkdir': 'True',  # BUGFIX 01
            'Content-Type': content_type,
        }
        content.seek(0)
        self.api.put(self._save_key(clean_name), content, headers=headers,
                     secret=self._secret)

        return clean_name

    def _open(self, name, mode):
        upyun_file = XZUpyunFile(name, self, mode)
        return upyun_file

    def get_available_name(self, name, max_length=None):
        # upyun 针对一个uri的api请求有时间间隔的限制，两次操作时间间隔为10s
        # 所以无法在一次业务操作内，包含多次请求操作，
        # 但允许覆盖上传，所以在这里直接沿用name，而不是检查后删除云端文件的上传覆盖
        return name


class XZUpyunFile(UpYunStorageFile):
    def thumbnail_url(self, version=None):
        return self._storage.thumbnail_url(self.name, version=version)


class XZUpyunStaticStorage(XZUpyunStorage):

    def __init__(self, **kwargs):
        root = setting('UPYUN_STATIC_ROOT', '/static')
        if 'root' in kwargs:
            kwargs.pop('root')
        super().__init__(root=root, **kwargs)
        dirs = self.listdir(root)[0]
        while len(dirs) != 0:
            path = dirs.pop()
            print(path)
            dirs.extend(self.listdir(path)[0])


class XZUpyunMediaStorage(XZUpyunStorage):
    def __init__(self, **kwargs):
        root = setting('UPYUN_MEDIA_ROOT', '/media')
        if 'root' in kwargs:
            kwargs.pop('root')
        super().__init__(root=root, **kwargs)
        dirs = self.listdir(root)[0]
        while len(dirs) != 0:
            path = dirs.pop()
            print(path)
            dirs.extend(self.listdir(path)[0])
