from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_choice, name='login_choice'),
    path('login/', views.login_choice, name='login_choice'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('owner/login/', views.owner_login, name='owner_login'),
    path('customer/register/', views.customer_register, name='customer_register'),
    path('owner/register/', views.owner_register, name='owner_register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
