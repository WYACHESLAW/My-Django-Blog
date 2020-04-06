from django.contrib import admin
from django.urls import path, include
#from django.urls import include, path  
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='')),
    path ('', include ('main.urls', namespace='')),
    #path('captcha/', include('captcha.urls')),
]
if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.МEDIA_URL, document_root = settings.МEDIA_ROOT)
    #import debug_toolbar
    urlpatterns = [
        #path('__debug__/',  include( debug_toolbar.urls)), 
          # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ]  +  urlpatterns