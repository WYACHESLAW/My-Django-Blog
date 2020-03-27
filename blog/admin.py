from django.contrib import admin
#from .models import AdvUser
from .forms import SubRubricForm
from .models import SuperRubric, SubRubric
from .models import Post, Comment

#admin.site.register(AdvUser)
admin.site.register(Post)
admin.site.register(Comment)
# Register your models here.
from .models import Projeсt

class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
    
admin.site.register(SuperRubric, SuperRubricAdmin)


 
class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ["id" ,"pr_title", "updated", "timestamp"]
    list_display_links = ["id", "updated"]
    list_editable = ["pr_title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "pr_content"]
    class Meta:
        model = Projeсt
 
admin.site.register(Projeсt, ProjectModelAdmin)