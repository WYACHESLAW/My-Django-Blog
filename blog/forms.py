from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

from .models import SuperRubric, SubRubric
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset = SuperRubric.objects.all(), empty_label=None, 
                                          label = 'Надрубрика', required = False)
    class Meta:
        model = SubRubric
        fields = '__all__'