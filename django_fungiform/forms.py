import fungiform
from fungiform.forms import *
from fungiform import widgets
from fungiform.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


__all__ = list(x for x in fungiform.forms.__all__ if x != 'FormBase')
__all__ += ['ValidationError', 'Form', 'widgets']


class Form(FormBase):

    def __init__(self, initial=None, action=None, request_info=None):
        # django explicitly passes the request around and so we don't use
        # _lookup_request_info if no request_info is passed in; we raise an
        # exception instead
        if request_info is None:
            msg = u'%s.request_info cannot be None' % self.__class__
            raise TypeError(msg)
        super(Form, self).__init__(initial, action, request_info)

    def _get_session(self):
        try:
            return self.request_info.session
        except AttributeError:
            msg = ('%r has no attribute "session". '
                    'Is a session middleware enabled?') % self.request_info
            raise AttributeError(msg)

    def _autodiscover_data(self):
        return getattr(self.request_info, self.request_info.method)

    def submitted_and_validate(self):
        if self.request_info.method == self.default_method:
            return self.validate()

    def _get_wsgi_environ(self):
        return self.request_info.environ

    def _resolve_url(self, args, kwargs):
        return reverse(*args, **kwargs)

    def _get_translations(self):
        # FIXME.actually return some translations
        return super(Form, self)._get_translations()

    def _redirect_to_url(self, url):
        return redirect(url)
