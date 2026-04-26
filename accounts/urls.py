from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # biometry
    path("webauthn/registration/", views.DeviceRegistration.as_view(), name="device_registration"),
    path("webauthn/devices/", views.DeviceListView.as_view(), name="device_list"),
    path("webauthn/devices/<int:pk>/delete/", views.DeleteDevice.as_view(), name="device_delete"),

    path('reg/', views.register, name='register'),
    path('signup', views.signup, name='signup'),
    path('register-init', views.register_init, name='register_init'),
    path('register-verify', views.register_verify, name='register_verify'),
    path('auth-init', views.auth_init, name='auth_init'),
    path('auth-verify', views.auth_verify, name='auth_verify'),
]
