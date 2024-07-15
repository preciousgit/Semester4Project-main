from django.urls import path
from . import views

# url patterns
urlpatterns = [
    path("", views.open_landing_page, name="open-landing"),
]
