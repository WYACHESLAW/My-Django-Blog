from django import forms
from .models import Post, Comment, Profile 
from .models import AdvUser
from django.contrib.auth import get_user_model

class ChangeUserinfoForm(forms.ModelForm):
    email = forms.EmailField(required = True, label = 'Aдpec электронной почты')
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model =  get_user_model()
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'author')

from .models import SuperRubric, SubRubric
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset = SuperRubric.objects.all(), empty_label=None, 
                                          label = 'Надрубрика', required = False)
    class Meta:
        model = SubRubric
        fields = '__all__'
class SearchForm(forms.Form):
    keyword = forms.CharField(required = False, max_length = 20, label = '')
    


        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)