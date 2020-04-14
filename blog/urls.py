from django.urls import path
from .import views
from .views import other_page
from .views import by_rubric, register
#from .views import RegisterDoneView
#from .views import user_activate
from django.contrib.auth import views as auth_views
from .views import profile
from .views import ChangeUserinfoView, STR_PasswordChangeView
from .views import profile_post_add
from .views import profile_post_change, profile_post_delete
from main.views import index

urlpatterns = [
#    path('logout/', auth_views.LoginView.as_view(), name='logout') ,
    path('profile/', profile, name='profile'),
    path('profile/add/', profile_post_add, name='profile_post_add'),
    path('profile/change/<int:pk>/', profile_post_change, name='profile_post_change'),
    path('profile/delete/<int:pk>/', profile_post_delete, name='profile_post_delete'),
#    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
#    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('register/', register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.post_list, name='post_list'),
    path('index', index, name='index'),
    #path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>', other_page, name='other'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('password/change/', STR_PasswordChangeView.as_view(), name='password_change'),
    path('profile/change/', ChangeUserinfoView.as_view(), name='change_user_info'),

]
