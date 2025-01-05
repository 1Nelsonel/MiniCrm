from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('crm.urls')),
    path('api/auth/', include('knox.urls')),
]
