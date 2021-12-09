from django.conf.urls import url
from django.urls import path
from accounts import views

urlpatterns = [
    path('user-register/',views.userRegister,name='userRegister'),

    path('user-login/', views.userLogin, name='userLogin'),
    path('admin-login/', views.adminLogin, name='adminLogin'),
    path('forgot-password/',views.forgotPassword, name='forgotPassword'),
    path('user-logout/', views.userLogout, name='userLogout'),
    path('admin-logout/', views.adminLogout, name='adminLogout'),
]
