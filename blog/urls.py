from django.urls import path
from . import views
from .views import other_page
from .views import by_rubric
#from .views import detail
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate

urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view (), name='register'),
    path('', views.post_list, name='post_list'),
    #path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
     path('<str:page>', other_page, name='other'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]
