from django.urls import path
from .views import index
from .views import document
from .views import st_detail, std_detail, profile_st_delete,profile_std_delete
from .views import profile_st_change, profile_std_change
from .views import login, profile_st_add, profile_std_add
from .views import st_edit, profile_st, profile_std, std_edit
from .views import by_rubric_st, by_rubric_std
app_name = 'main'

urlpatterns = [
path('accounts/login', login, name='login'),

path('profile_st/delete/<int:pk>/', profile_st_delete, name='profile_st_delete'),
path('profile_std/delete/<int:pk>/', profile_std_delete, name='profile_std_delete'),
path('profile_st/change/<int:pk>/', profile_st_change, name='profile_st_change'),
path('profile_std/change/<int:pk>/', profile_std_change, name='profile_std_change'),
path('profile_st/add/', profile_st_add, name='profile_st_add'),
path('profile_std/add/', profile_std_add, name='profile_std_add'),
path('<int:pk>/st_detail/', st_detail, name='st_detail'),
path('<int:pk>/std_detail/', std_detail, name='std_detail'),
path('profile_st/', profile_st, name='profile_st'),
path('profile_std/', profile_std, name='profile_std'),
path('<int:pk>/by_rubric_st/', by_rubric_st, name='by_rubric_st'),
path('<int:pk>/', by_rubric_std, name='by_rubric_std'),
path('accounts/document', document, name='document'),
path('<int:pk>/st_edit/', st_edit, name='st_edit'),
path('std_edit/<int:pk>/', std_edit, name='std_edit'),
path('', index, name='index'),
]
