from django.urls import path
from .views import index
from .views import document
from .views import st_rubric
from .views import st_detail
from .views import doc_detail
from .views import login
from .views import st_edit
app_name = 'main'

urlpatterns = [
path('<int:pk>/accounts/st_detail', st_detail, name='st_detail'),
path('<int:pk>/', st_rubric, name='st_rubric'),
path('', index, name='index'),
path('accounts/login', login, name='login'),
path('accounts/document', document, name='document'),
path('<int:pk>/accounts/docdetail', doc_detail, name='docdetail'),
 path('<int:pk>/edit/', st_edit, name='st_edit'),
]