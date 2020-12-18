from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import UserProfile, User, SignUpVerification, Client, Country, Store, Image
from django.http import JsonResponse
from .utils import (
    UserCreationValidation,
    send_registration_confirm_mail,
    get_permission_for_app,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


class HomeView(LoginRequiredMixin, View):
    template = "home.html"
    login_url = "user:signin"

    def get(self, request):
        return render(request, self.template)


class CreateUserView(
    LoginRequiredMixin, PermissionRequiredMixin, View, UserCreationValidation
):
    template = "create-user.html"
    login_url = "user:signin"
    permission_required = "user.add_user"

    def get(self, request):
        context = {"types": UserProfile.TYPE_CHOICES}
        return render(request, self.template, context)

    def post(self, request):
        user = self.create_user(request.POST)
        if isinstance(user, User):
            Image.objects.create(user=user, image=request.FILES["profile-image"])
            user_profile = UserProfile.objects.create(
                user=user,
                phone_number=self.phone,
                position=request.POST["position"],
                user_type=request.POST["user-type"],
                created_by=request.user,
                modified_by=request.user,
                allowed_clients={"clients": []},
                allowed_countries={"countries": []},
                allowed_stores={"stores": []},
            )
            code, created = SignUpVerification.objects.get_or_create(user=user)
            host = request.headers["Host"]
            url = f"http://{host}/verify-user/{code.uid}"
            redirect_url = f"http://{host}/add-user-permissions/{user.id}"
            send_registration_confirm_mail([user.email], url)

            return JsonResponse(
                status=201, data={"redirect_url": redirect_url}, safe=False
            )
        return JsonResponse(status=400, data=user, safe=False)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template = "user-list.html"
    login_url = "user:signin"
    permission_required = "user.view_user"

    def get(self, request):
        users = User.objects.all().exclude(is_superuser=True)
        context = {"users": users}
        return render(request, self.template, context)


class AddUserPermissions(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "user:signin"
    template = "add-user-permissions.html"
    permission_required = ("user.change_user", "user.change_userprofile")

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        clients = Client.objects.filter(is_active=True)
        countries = Country.objects.filter(is_active=True)
        stores = Store.objects.all()
        permissions = get_permission_for_app("user")
        context = {
            "clients": clients,
            "countries": countries,
            "stores": stores,
            "permissions": permissions,
            "user": user,
        }
        return render(request, self.template, context)


class EditUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template = "edit-user.html"
    login_url = "user:signin"
    permission_required = "user.change_user"

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        user_types = UserProfile.TYPE_CHOICES
        context = {"user": user, "types": user_types}
        return render(request, self.template)
