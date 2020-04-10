from django.contrib import admin
from .forms import StSubRubricForm, StDSubRubricForm
from .models import StDocument, St
from .models import StSuperRubric, StSubRubric, StDSuperRubric, StDSubRubric


class StSubRubricInline(admin.TabularInline):
    model = StSubRubric

class StDSubRubricInline(admin.TabularInline):
    model = StDSubRubric

class StSuperRubricAdmin(admin.ModelAdmin):
    exclude = ('stsuper_rubric',)
    inlines = (StSubRubricInline,)

class StDSuperRubricAdmin(admin.ModelAdmin):
    exclude = ('stdsuper_rubric',)
    inlines = (StDSubRubricInline,)

class StSubRubricAdmin(admin.ModelAdmin):
    form = StSubRubricForm
    
class StDSubRubricAdmin(admin.ModelAdmin):
    form = StDSubRubricForm

#class AdditionalImageInline(admin.TabularInline):
#    model = AdditionalImage
    
class StAdmin(admin.ModelAdmin):
    list_display = ('strubric', 'title', 'content', 'author', 'created_at')
    fields = (('strubric', 'author'), 'title', 'content', 'price',
               'contacts', 'is_active')
    #inlines = (AdditionalImageInline,)
    
class StDAdmin(admin.ModelAdmin):
    list_display = ('stdrubric', 'title', 'content', 'author', 'created_at')
    fields = (('stdrubric', 'author'), 'title', 'content', 'price',
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
admin.site.register(StSuperRubric, StSuperRubricAdmin)
admin.site.register(StSubRubric, StSubRubricAdmin)
admin.site.register(StDSuperRubric, StDSuperRubricAdmin)
admin.site.register(StDSubRubric, StDSubRubricAdmin)  
