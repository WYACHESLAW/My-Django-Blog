from django.contrib import admin
from .forms import SubRubricForm
from .models import SuperRubric, SubRubric
from .models import Post, Comment
from .models import AdvUser


class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
            modeladmin.message_user(request, 'Письма с оповещениями отправлены')
            send_activation_notifications.short_description = 'Отправка писем с ' + \
            'оповещениями об активации'

class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    pararneter_name = 'actstate'
    def lookups(self, request, model_admin):
        return (
               ('activated', 'Прошли'), ('threedays', 'Не прошли более 3 дней'),
               ( 'week' , 'Не прошли более недели' ) ,
               )
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active = True, is_activated = True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days = З)
            return queryset.filter(is_active= False, is_activated = False, date_joined__date__lt = d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks = 1)
            return queryset.filter(is_active = False, is_activated = False, date_joined__date__lt = d)

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,) 

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'price', 'published']
    list_display_links = ['title', 'content']
    search_fields = ['title', 'content',]
 
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(AdvUser)