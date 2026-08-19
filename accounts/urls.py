from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ThrottledLoginView

app_name = 'accounts'
urlpatterns = [
    path('login/', ThrottledLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password/done/'), name='password_change'),
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_done.html'), name='password_done'),
]
