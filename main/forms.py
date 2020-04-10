from django import forms
from .models import St, StDocument
from .models import Comment
from .models import StSuperRubric, StSubRubric, StDSuperRubric, StDSubRubric

class StSubRubricForm(forms.ModelForm):
    stsuper_rubric = forms.ModelChoiceField(queryset = StSuperRubric.objects.all(), empty_label=None, 
                                          label = 'Надрубрика', required = False)
    class Meta:
        model = StSubRubric
        fields = '__all__'
        
class StDSubRubricForm(forms.ModelForm):
    stdsuper_rubric = forms.ModelChoiceField(queryset = StDSuperRubric.objects.all(), empty_label=None, 
                                          label = 'Надрубрика', required = False)
    class Meta:
        model = StDSubRubric
        fields = '__all__'
        
class SearchForm(forms.Form):
    keyword = forms.CharField(required = False, max_length = 20, label = '')
    
class StForm(forms.ModelForm):
    class Meta:
        model = St
        fields = '__all__'
        widgets = {'author':forms.HiddenInput}
#AIFormSet = inlineformset_factory(St, fields='__all__')

class StDocumentForm(forms.ModelForm):
    class Meta:
        model = StDocument
        fields = '__all__'
        widgets = {'author':forms.HiddenInput}
#AIFormSet = inlineformset_factory(St, fields='__all__')
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'st':forms.HiddenInput}


