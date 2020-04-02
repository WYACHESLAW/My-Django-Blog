from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name = 'Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name = 'Слать оповещение о новых коментариях ?')
    def delete(self, *arqs, **kwarqs):
        for post in self.post_set.all():
            post. delete()
            super().delete(*arqs, **kwarqs)
    class Meta(AbstractUser.Meta):
        pass

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

class Post(models.Model):
    rubric = models.ForeignKey(SubRubric, null=True, on_delete=models.PROTECT, verbose_name = 'Pyбpикa')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    is_active = models.BooleanField(default = True, db_index = True, verbose_name = 'Выводить в списке?')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


        
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text