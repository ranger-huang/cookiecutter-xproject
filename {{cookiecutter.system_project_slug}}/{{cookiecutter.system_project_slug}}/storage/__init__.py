from os.path import join

from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.files.storage import FileSystemStorage
from django.utils._os import abspathu
from django.utils.encoding import force_text


def unsafe_join(base, *paths):
    base = force_text(base)
    paths = [force_text(p) for p in paths]
    final_path = abspathu(join(base, *paths))
    #base_path = abspathu(base)
    return final_path


class XZLocalStorageMixin(object):
    def _clean_path(self, name):
        return name.lstrip("/")

    def path(self, name):
        # django 1.10.1 只能在跟应用目录下使用文件路径，超出根目录外则会报错误
        # 所以在此以重载方式使用，以保持项目文件结构
        # FIXIT django.utils._os.safe_join raise SuspiciousFileOperation
        return unsafe_join(self.location, self._clean_path(name))

    def get_available_name(self, name, max_length=None):
        name = self._clean_path(name)
        if self.exists(name):
            self.delete(name)
        return name


class XZLocalStorage(XZLocalStorageMixin, FileSystemStorage):
    pass


class XZLocalStaticStorage(XZLocalStorageMixin, StaticFilesStorage):
    pass


