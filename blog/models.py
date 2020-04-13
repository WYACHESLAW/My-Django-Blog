from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name = 'Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name = 'Слать оповещение о новых коментариях ?')
    def delete(self, *arqs, **kwarqs):
        for st in self.st_set.all():
            st. delete()
            super().delete(*arqs, **kwarqs)
    class Meta(AbstractUser.Meta):
        pass
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


    
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
        verbose_name = 'Подрубрика тем'
        verbose_name_plural = 'Подрубрики тем'

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
        verbose_name = 'Надрубрика тем'
        verbose_name_plural = 'Надрубрики тем'

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
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, 
 	                   self.publish.month, self.publish.day, self.slug])
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