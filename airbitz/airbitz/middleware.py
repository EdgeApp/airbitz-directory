import settings

class SetRemoteAddr(object):
    def process_request(self, request):
        self.from_forwarded_ip(request)
        self.from_real_ip(request)

    def from_forwarded_ip(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip

    def from_real_ip(self, request):
        try:
            real_ip = request.META['HTTP_X_REAL_IP']
        except KeyError:
            pass
        else:
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip


class SessionExpiry(object):
    def process_request(self, request):
        if getattr(settings, 'SESSION_EXPIRY', None):
            if request.user.is_superuser:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(settings.SESSION_EXPIRY)
        return None
