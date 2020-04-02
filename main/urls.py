from django.urls import path
from .views import index
from .views import other_page
from .views import STR_LoginView
from .views import document
from .views import STR_LogoutView
from .views import ChangeUserinfoView
from .views import STR_PasswordChangeView
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import DeleteUserView
from .views import by_rubric
from .views import detail
app_name = 'main'

urlpatterns = [
path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),        
path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
path('accounts/register/', RegisterUserView.as_view (), name='register'),
path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
path('<int:pk>/', by_rubric, name='by_rubric'),
path('<str:page>', other_page, name='other'),
path('accounts/', document, name='document'),
path('', index, name='index'),
path('accounts/login/', STR_LoginView.as_view(), name='login'),
path('accounts/logout/', STR_LogoutView.as_view (), name='logout'),
path('accounts/profile/change/', ChangeUserinfoView.as_view(), name='profile_change'),
path('accounts/password/change/', STR_PasswordChangeView.as_view(), name='password_change'),
]