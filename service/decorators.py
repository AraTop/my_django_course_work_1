from django.shortcuts import redirect
from service.models import Token

def token_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.GET.get('token')  # Можете выбрать другой способ передачи токена в запросе
        if not token or not Token.objects.filter(key=token).exists():
            return redirect('access_denied_url')  # Замените 'access_denied_url' на URL страницы с сообщением об отказе в доступе
        return view_func(request, *args, **kwargs)
    return _wrapped_view