from django import forms
from .models import AdvUser

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import St
from captcha.fields import CaptchaField
from .models import Comment

        
from .models import SuperRubric, SubRubric

class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset = SuperRubric.objects.all(), empty_label=None, 
                                          label = 'Надрубрика', required = False)
    class Meta:
        model = SubRubric
        fields = '__all__'
        
class SearchForm(forms.Form):
    keyword = forms.CharField(required = False, max_length = 20, label = '')
    
class StForm(forms.ModelForm):
    class Meta:
        model = St
        fields = '__all__'
        widgets = {'author':forms.HiddenInput}
#AIFormSet = inlineformset_factory(St, fields='__all__')

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'st':forms.HiddenInput}

class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки',
              error_messages={'invalid':'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'st': forms.HiddenInput}
