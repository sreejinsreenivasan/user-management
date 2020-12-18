from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from typing import Dict
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse, Http404
from user.models import SignUpVerification
from django.db import transaction


class SignInView(View):
    template = "sign-in.html"

    def validate(self, creds: Dict) -> Dict:
        for key, value in creds.items():
            if len(value) == 0:
                return f"{key} should not be empty"
        return creds

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        validated_data = self.validate({"username": username, "password": password})

        if not type(validated_data) == dict:
            messages.add_message(request, messages.WARNING, validated_data)
            return redirect("user:signin")

        user = authenticate(username=username, password=password)
        print(user)
        if user and user is not None:
            login(request, user)
            remember_me = request.POST.get("remember_me", False)
            session_expiry = 1209600 if remember_me else 0
            print(session_expiry)
            request.session.set_expiry(session_expiry)
            return redirect("user:home")

        else:
            messages.add_message(request, messages.ERROR, "Wrong credentials")
            return redirect("user:signin")


def Logout(request):
    logout(request)
    return redirect("user:home")


class VerifyUser(View):
    template = "verify-user.html"

    def get(self, request, id):
        if request.user.is_authenticated:
            return redirect("user:home")
        try:
            code = get_object_or_404(SignUpVerification, uid=id)
        except ValidationError:
            raise Http404()
        return render(request, self.template, {"uid": code.uid})

    def post(self, request, id):
        password = request.POST["password"]
        confirm_password = request.POST["password_confirm"]
        if not password == confirm_password:
            return JsonResponse(status=400, data="Passwords do not match", safe=False)
        try:
            code = get_object_or_404(SignUpVerification, uid=id)
            user = code.user
            with transaction.atomic():
                user.is_active = True
                user.set_password(password)
                user.save()
                code.delete()
                login(request, user)
                return JsonResponse(status=200, data="Successfully Verfied", safe=False)
        except ValidationError:
            raise Http404()
