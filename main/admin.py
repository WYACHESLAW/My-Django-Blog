from django.contrib import admin
from .models import AdvUser
from .forms import SubRubricForm
import datetime
from .utilities import send_activation_notification
from .models import StDocument
from .models import SuperRubric, SubRubric
from .models import St

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

class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
    


#class AdditionalImageInline(admin.TabularInline):
#    model = AdditionalImage
    
class StAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price',
               'contacts', 'is_active')
    #inlines = (AdditionalImageInline,)
    
#@admin.register(StDocument)
class DocumAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('d_title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
admin.site.register(StDocument)
admin.site.register(St, StAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin) 
