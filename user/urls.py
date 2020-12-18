from django.urls import path
from .views import (
    CreateUserView,
    UserListView,
    HomeView,
    AddUserPermissions,
    EditUserView,
)
from .auth import SignInView, VerifyUser, Logout

app_name = "user"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("create-user", CreateUserView.as_view(), name="createuser"),
    path(
        "add-user-permissions/<int:pk>",
        AddUserPermissions.as_view(),
        name="add_user_permissions",
    ),
    path("user-list", UserListView.as_view(), name="userlist"),
    path("sign-in", SignInView.as_view(), name="signin"),
    path("sign-out", Logout, name="logout"),
    path("verify-user/<str:id>", VerifyUser.as_view()),
    path("edit-user/<int:pk>", EditUserView.as_view(), name="edituser"),
]
