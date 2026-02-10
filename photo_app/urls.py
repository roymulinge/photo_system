from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PasswordChangeView

urlpatterns = [
    
    
path(
    "password/change/",
    PasswordChangeView.as_view(
        template_name="accounts/password_change.html",
        success_url="/profile/"  
    ),
    name="password_change",
),

    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("photo/<int:photo_id>/", views.photo_detail, name="photo_detail"),
    path("photo/<int:photo_id>/like/", views.toggle_like, name="toggle_like"),
    path("upload/", views.upload_photo, name="upload_photo"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]