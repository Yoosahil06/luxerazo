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
    path('users/', include('users.urls')),
    path('brands/', include('brands.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('dashboard/', include('dashboard.urls')),
    # path('content/', include('content.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
