from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('accounts/', include('accounts.urls')),  
    
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', views.home, name='home'),
]
