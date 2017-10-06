from django.http.response import HttpResponseRedirectBase
from rest_framework.response import Response
from rest_framework import status


class XLocationResponse(HttpResponseRedirectBase, Response):

    status_code = status.HTTP_302_FOUND

    def __init__(self, redirect_to, *args, **kwargs):
        HttpResponseRedirectBase.__init__(self, redirect_to, *args, **kwargs)
        location = self['Location']
        Response.__init__(self, *args, **kwargs)
        self['Location'] = location

    @property
    def rendered_content(self):
        if self.data is None:
            return None
        return super().rendered_content


class XRawResponse(Response):

    @property
    def rendered_content(self):
        if self.content_type:
            self['Content-Type'] = self.content_type
        return self.data
