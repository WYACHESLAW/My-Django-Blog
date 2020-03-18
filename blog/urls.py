from django.urls import path
from . import views
from .views import other_page
from .views import by_rubric
#from .views import detail

urlpatterns = [
    path('<str:page>', other_page, name='other'),
    path('', views.post_list, name='post_list'),
    #path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]
