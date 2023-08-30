from django.db import models
from users.models import User

NULLABLE = {'null':True, 'blank':True}

class Blog(models.Model):
   header = models.CharField(max_length=250 ,verbose_name='заголовок')
   content = models.TextField(verbose_name='содержимое статьи')
   image = models.ImageField( verbose_name='Изображение', **NULLABLE)
   publication_date = models.DateField(verbose_name='Дата публикации')
   views = models.IntegerField(verbose_name='Количество просмотров', default=0)


   def __str__(self):
      return f'{self.header} {self.content}' 
   
   class Meta:
      verbose_name = 'Блог'
      verbose_name_plural = 'Блоги'
      ordering = ('header',)