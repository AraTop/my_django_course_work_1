from django.urls import path
from django.urls import path
from service import views
app_name = 'service'

urlpatterns = [
   path("", views.CustomerListView.as_view()),
   path("create/", views.CustomerCreateView.as_view()),
   path("delete/<int:pk>/", views.CustomerDeleteView.as_view()),
   path("update/<int:pk>/", views.CustomerUpdateView.as_view()),
   path("<int:pk>/", views.CustomerDetailView.as_view(), name='service'),
   path("settings/", views.SettingsListView.as_view()),
   path("settings/create/", views.SettingsCreateView.as_view()),
   path("settings/delete/<int:pk>/", views.SettingsDeleteView.as_view()),
   path("settings/update/<int:pk>/", views.SettingsUpdateView.as_view()),
   path("settings/<int:pk>/", views.SettingsDetailView.as_view(), name='settings'),
   path("message/", views.Message_to_SendListView.as_view()),
   path("message/create/", views.Message_to_SendCreateView.as_view()),
   path("message/delete/<int:pk>/", views.Message_to_SendDeleteView.as_view()),
   path("message/update/<int:pk>/", views.Message_to_SendUpdateView.as_view()),
   path("message/<int:pk>/", views.Message_to_SendDetailView.as_view(), name='message'),
   path("logs/", views.Mailing_LogsListView.as_view()),
   path("logs/create/", views.Mailing_LogsCreateView.as_view()),
   path("logs/delete/<int:pk>/", views.Mailing_LogsDeleteView.as_view()),
   path("logs/update/<int:pk>/", views.Mailing_LogsUpdateView.as_view()),
   path("logs/<int:pk>/", views.Mailing_LogsDetailView.as_view(), name='logs'),
]