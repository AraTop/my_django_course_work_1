from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView
from users.models import User
from users.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from project import settings
from django.shortcuts import redirect
from .permissions import  ModeratorPermissionsMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView


class LoginView(BaseLoginView):
   template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
   pass


def is_in_moderator_group(user):
   return user.is_authenticated and user.groups.filter(name='moderator').exists()

class RegisterView(CreateView):
   model = User
   form_class = UserForm
   template_name = 'users/users_register.html'
   success_url = '/users/login/'

   def form_valid(self, form):
      response = super().form_valid(form)
      token = default_token_generator.make_token(self.object)
      confirmation_url = self.request.build_absolute_uri(reverse_lazy('users:verify_email', args=[token]))
      self.object.email_confirmation_token = token
      self.object.save()
      send_mail(
         subject='Подтвердите ваш адрес электронной почты',
         message=f'Пожалуйста нажмите на следующую ссылку, чтобы подтвердить свой адрес электронной почты: {confirmation_url}',
         from_email=settings.EMAIL_HOST_USER,
         recipient_list=[self.object.email]
      )
      return response

@method_decorator(login_required, name='dispatch')  
class VerifyEmail(TemplateView):
   def get(self, request, *args, **kwargs):
     print(request.user.email_confirmation_token)
     key = request.user.email_confirmation_token
     user = User.objects.filter(email_confirmation_token=key).first()
     if user:
         request.user.is_email_verified = True
         request.user.email_confirmation_token = None
         request.user.save()
         return redirect('/') 
     else:
         return redirect('/error-page/')
     
@method_decorator(login_required, name='dispatch')  
class ProfileView(UpdateView):
   model = User
   form_class = UserProfileForm
   success_url = reverse_lazy("users:profile")

   def get_object(self, queryset=None):
      return self.request.user
#----------------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class UsersListView(UserPassesTestMixin, ListView):
   model = User
   template_name = 'users/users_list.html'

   def test_func(self):
      return self.request.user.groups.filter(name='moderator').exists()

@method_decorator(login_required, name='dispatch')
class UserDetailView(ModeratorPermissionsMixin, DetailView):
   model = User
   template_name = 'users/user_detail.html'
