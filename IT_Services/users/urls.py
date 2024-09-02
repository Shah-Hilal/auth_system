from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name = 'home'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/<int:pk>/update/', views.update_service, name='update_service'),
    path('services/<int:pk>/delete/', views.delete_service, name='delete_service'),
    path('services/<int:pk>/subscribe/', views.subscribe, name='subscribe'),
    path('callback/', views.callback, name='callback'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
