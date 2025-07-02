from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # homepage, about, etc.
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('account/', include('users.urls')),
    path('brands/', include('brands.urls')),
    path('concierge/', include('concierge.urls')),
    path('catalog/', include('catalog.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('dashboard/', include('dashboard.urls')),
    # path('content/', include('content.urls')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
