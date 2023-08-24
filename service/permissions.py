from django.contrib.auth.models import Group
from django.shortcuts import render

class AuthorPermissionsMixin:
    def has_permissions(self):
        return self.get_object().client_id == self.request.user.id
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'service/access_denied.html')
        return super().dispatch(request, *args, **kwargs)

class AuthorMessagePermissionsMixin:
    def has_permissions(self):
        return self.get_object().settings.client_id == self.request.user.id
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'service/access_denied.html')
        return super().dispatch(request, *args, **kwargs)
    
class ModeratorPermissionsMixin(AuthorPermissionsMixin):
    def has_permissions(self):
        is_author = super().has_permissions()

        if is_author:
            return True

        return self.request.user.groups.filter(name='moderator').exists()
    
class ModeratorMessagePermissionsMixin(AuthorMessagePermissionsMixin):
    def has_permissions(self):
        is_author = super().has_permissions()

        if is_author:
            return True

        return self.request.user.groups.filter(name='moderator').exists()