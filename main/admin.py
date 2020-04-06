from django.contrib import admin
from .forms import SubRubricForm
from .models import StDocument
from .models import SuperRubric, SubRubric
from .models import St

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
    list_display = ('title', 'slug', 'body', 'author', 'publish','status')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('d_title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
admin.site.register(StDocument)
admin.site.register(St, StAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin) 
