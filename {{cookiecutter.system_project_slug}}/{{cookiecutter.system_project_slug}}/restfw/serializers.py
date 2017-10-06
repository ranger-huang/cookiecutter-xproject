# -*- coding: utf-8 -*-


class XResponseResult(dict):

    def __init__(self, code, data=None, msg=None, **kwargs):
        super().__init__(**kwargs)
        self.code = self['code'] = code
        self.data = self['data'] = data
        self.msg = self['msg'] = msg or ''


