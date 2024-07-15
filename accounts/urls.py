from django.urls import path
from . import views

# url patterns
urlpatterns = [
    path("verifylogin/", views.verify_users_credentials, name="verif-login"),
    path("registeruser/", views.sign_up, name="sign-up"),
    path("changepassword/", views.forgot_password, name="forgot-password"),
    path("readbook/", views.read_book, name="read-book"),
    path("watchbook", views.watch_video, name="watch-video"),
    path('logout/', views.logout_view, name='logout'),
]
