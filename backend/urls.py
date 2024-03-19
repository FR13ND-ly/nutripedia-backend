from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path('api/files/', include('file.urls')),
    path('api/products/', include('product.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/suggestions/', include('suggestion.urls')),
    path('api/users/', include('user.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
