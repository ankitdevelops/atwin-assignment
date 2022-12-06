from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("update_score", views.update_score, name="update_score"),
]
