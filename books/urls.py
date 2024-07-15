from django.urls import path
from . import views

# url patterns
urlpatterns = [
    path("home/", views.open_home_page, name="home-page"),
    path("login/", views.open_login_page, name="login-page"),
    path("searchbooks/", views.search_books, name="search-books"),
    path("makenquires/", views.get_inquiries_user, name="enqiry-for-admin"),
    path("authsearch/", views.auth_search_books, name="auth-search"),
    path('report/', views.report, name='report'),
]
