from django.contrib import admin
from .models import Post
#from .models import AdvUser
from .forms import SubRubricForm
from .models import SuperRubric, SubRubric

#admin.site.register(AdvUser)
admin.site.register(Post)
# Register your models here.
class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
    
admin.site.register(SuperRubric, SuperRubricAdmin)