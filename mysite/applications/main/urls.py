from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.main, name = "main"),
    path("contact/", views.emailView, name = "contact"),
    path("contact/sent/", views.successView, name = "sent"),
]
