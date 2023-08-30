import random
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView
from main.models import Blog
from service.models import Settings


def home_page(request):
   object_list_count = Settings.objects.all().count()
   all_Blogs = Blog.objects.all()

   if len(all_Blogs) <= 3:
      random_articles = all_Blogs
   else:
      random_articles = random.sample(list(all_Blogs), 3)

   active_newsletters_count = Settings.objects.filter(mailing_status__in=['создана', 'запущена']).count()
   unique_clients_count = Settings.objects.values('client').distinct().count()
   context = {
      'active_newsletters_count': active_newsletters_count,
      'unique_clients_count': unique_clients_count,
      'object_list_count': object_list_count,
      'publications': random_articles
   }

   return render(request, 'main/main_page.html', context)