from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification
from .utilities import get_timestamp_path
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import AdvUser

    
user_registrated = Signal(providing_args = ['instance'])
def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
    user_registrated.connect(user_registrated_dispatcher)
    
class Rubric(models.Model):
    name = models.CharField(max_length = 20, db_index = True, null = True, unique = True, verbose_name = 'Haзвaниe')
    order = models.SmallIntegerField(default = 0, db_index = True, verbose_name = 'Пopядoк')
    super_rubric = models.ForeignKey('SuperRubric',
                                     on_delete = models.PROTECT, null = True, blank = True,
                                     verbose_name = 'Haдpyбpикa')
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects = SuperRubricManager()
    
    def __str__(self):
        return self.name
    
    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'
        

class SubRubricМanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull = False)
    
class SubRubric(Rubric):
    objects = SubRubricМanager()
    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)
    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
       

class St(models.Model):
    rubric = models.ForeignKey(SubRubric, null=True, on_delete=models.PROTECT, verbose_name = 'Pyбpикa')
    title = models.CharField(max_length = 40, verbose_name = 'Tема')
    content = models.TextField(verbose_name = 'Oпиcaниe')
    price = models.CharField(max_length = 40, verbose_name='Станок')
    contacts = models.TextField(verbose_name = 'Koнтaкты')
    image = models.ImageField(blank = True, upload_to = get_timestamp_path, verbose_name = 'Изображение')
    author = models.ForeignKey(AdvUser, on_delete = models.CASCADE, verbose_name = 'Aвтop объявления')
    is_active = models.BooleanField(default = True, db_index = True, verbose_name = 'Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликовано')
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai. delete ()
        super().delete(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявления'
        ordering = ['-created_at']

class StDocument(models.Model):
    STATUS_CHOICES = ( 
                     ('draft', 'Draft'), 
                     ('published', 'Published'), 
) 
    title = models.CharField(max_length=250, default='', verbose_name = 'Tема') 
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', default='0000', verbose_name ='Код') 
    author = models.ForeignKey(AdvUser, 
                               on_delete=models.CASCADE,
                               related_name='main_documents', default='', verbose_name = 'Автор') 
   
    publish = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликовано')
    status = models.CharField(max_length=10,  
                              choices=STATUS_CHOICES, 
                              default='draft') 
    
    objects = models.Manager() # The default manager. 
    published = PublishedManager() # Our custom manager.
    class Meta: 
        ordering = ('-publish',) 
    def __str__(self): 
        return self.title
    def get_absolute_url(self):
        return reverse('main:document',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
       
#class AdditionalImage(models.Model):
#    st = models.ForeignKey(St, on_delete = models.CASCADE, verbose_name = 'Объявление')
#    image = models.ImageField(upload_to = get_timestamp_path, verbose_name = 'Изображение')
#    class Meta:
#        verbose_name_plural = 'Дополнительные иллюстрации'
#        verbose_name = 'Дополнительная иллюстрация'
       
class Comment(models.Model):
    st = models.ForeignKey(St, on_delete = models.CASCADE, verbose_name = 'Объявление')
    author = models.CharField(max_length=30, verbose_name='Aвтop' )
    content = models.TextField(verbose_name='Coдepжaниe')
    is_active = models.BooleanField(default = True, db_index = True, verbose_name = 'Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликован')
    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-created_at']

from django.db.models.signals import post_save
def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])
post_save.connect(post_save_dispatcher, sender=Comment)




