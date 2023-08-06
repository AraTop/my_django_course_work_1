from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from service.models import Customer_Service, Settings, Message_to_Send, Mailing_Logs 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class CustomerCreateView(CreateView):
   model = Customer_Service
   fields = ('email', 'last_name', 'first_name', 'surname', 'comment', 'password')
   success_url = '/accounts/login/'

   def form_valid(self, form):
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      return super().form_valid(form)

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
   model = Customer_Service
   success_url = '/service' 

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class CustomerListView(LoginRequiredMixin, ListView):
   model = Customer_Service

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class CustomerDetailView(LoginRequiredMixin, DetailView):
   model = Customer_Service
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
   model = Customer_Service
   fields = ('email', 'last_name', 'first_name', 'surname', 'comment', 'password')
   success_url = '/service'

   def form_valid(self, form):
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      return super().form_valid(form)

   def get_success_url(self):
      return reverse('service:service', args=[self.kwargs.get('pk')])
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
#---------------------------------------------------------------------------

class SettingsCreateView(LoginRequiredMixin, CreateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Customer_Service.objects.all()
      context['objects'] = settings_objects
      return context

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class SettingsDeleteView(LoginRequiredMixin, DeleteView):
   model = Settings
   success_url = '/service/settings/' 

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class SettingsListView(LoginRequiredMixin, ListView):
   model = Settings

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class SettingsDetailView(LoginRequiredMixin, DetailView):
   model = Settings

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class SettingsUpdateView(LoginRequiredMixin, UpdateView):
   model = Settings
   fields = ('mailing_time', 'periodicity', 'mailing_status', 'client')
   success_url = '/service/settings/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Customer_Service.objects.all()
      context['objects'] = settings_objects
      return context
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
#--------------------------------------------------------------

class Message_to_SendCreateView(LoginRequiredMixin, CreateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class Message_to_SendDeleteView(LoginRequiredMixin, DeleteView):
   model = Message_to_Send
   success_url = '/service/message/' 

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)

class Message_to_SendListView(LoginRequiredMixin, ListView):
   model = Message_to_Send

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class Message_to_SendDetailView(LoginRequiredMixin, DetailView):
   model = Message_to_Send
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   

class Message_to_SendUpdateView(LoginRequiredMixin, UpdateView):
   model = Message_to_Send
   fields = ('letter_subject', 'letter_body', 'settings')
   success_url = '/service/message/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
#--------------------------------------------------------------

class Mailing_LogsCreateView(LoginRequiredMixin, CreateView):
   permission_classes = [IsAuthenticated]
   model = Mailing_Logs
   fields = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')
   success_url = '/service/logs/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class Mailing_LogsDeleteView(LoginRequiredMixin, DeleteView):
   permission_classes = [IsAuthenticated]
   model = Mailing_Logs
   success_url = '/service/logs/' 

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class Mailing_LogsListView(LoginRequiredMixin, ListView):
   permission_classes = [IsAuthenticated]
   model = Mailing_Logs

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class Mailing_LogsDetailView(LoginRequiredMixin, DetailView):
   permission_classes = [IsAuthenticated]
   model = Mailing_Logs
   
   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
   
class Mailing_LogsUpdateView(LoginRequiredMixin, UpdateView):
   permission_classes = [IsAuthenticated]

   model = Mailing_Logs
   fields = ('date_and_time_of_last_attempt', 'attempt_status', 'mail_server_response', 'settings')
   success_url = '/service/logs/'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      settings_objects = Settings.objects.all()
      context['objects'] = settings_objects
      return context

   def dispatch(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return self.handle_no_permission()
      return super().dispatch(request, *args, **kwargs)
#--------------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            response = redirect('/service/')
            response['Authorization'] = f'Bearer {access}'
            response.set_cookie('access_token', access, httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
   response = JsonResponse({"message": "Logout completed successfully"})
   response.delete_cookie('access_token')
   response.delete_cookie('refresh_token')
   return response