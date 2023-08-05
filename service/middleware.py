from django.utils.deprecation import MiddlewareMixin

class UniqueSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if request.user.is_authenticated:
            session_key = f'{user_agent}:{request.user.pk}'
        else:
            ip_address = request.META.get('REMOTE_ADDR', '')
            session_key = f'{user_agent}:{ip_address}'
        
        if session_key and request.session.session_key != session_key:
            request.session.flush()
            request.session.cycle_key()
            request.session.create()