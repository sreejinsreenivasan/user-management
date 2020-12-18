from django.urls import path
from .views import UserDetailView, UserProfileDetailView

app_name = "api"

urlpatterns = [
    path("user/<int:pk>", UserDetailView.as_view()),
    path("user-profile/<int:pk>", UserProfileDetailView.as_view()),
]
