from django.urls import path
from accounts import views

urlpatterns = [
    path('user-register/',views.userRegister,name='userRegister'),

    path('user-login/', views.userLogin, name='userLogin'),
    path('admin-login/', views.adminLogin, name='adminLogin'),
    path('forgot-password/',views.forgotPassword, name='forgotPassword'),
    path('forgot-password-admin/', views.forgotPasswordAdmin, name='forgotPasswordAdmin'),
    path('user-logout/', views.userLogout, name='userLogout'),
    path('admin-logout/', views.adminLogout, name='adminLogout'),
    path('user-dashboard/',views.dashboardUser,name='dashboardUser'),
    path('admin-dashboard/',views.dashboardAdmin,name='dashboardAdmin')
]
