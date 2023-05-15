from django.urls import path
from Zing_It_App import views

urlpatterns = [
    path('', views.index, name="index"),
    path("playlist/<int:n>/", views.playlist, name="playlist"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("edit/<int:id>", views.edit, name="edit")
]
