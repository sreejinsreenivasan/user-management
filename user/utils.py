import re, string
from typing import Dict, List
from .models import User, UserProfile, Image
from django.db.utils import IntegrityError
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from decouple import config
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from .apps import AppConfig


class UserCreationValidation:
    name = ""
    username = ""
    email = ""
    phone = ""
    name_error = ""
    username_error = ""
    email_error = ""
    phone_error = ""
    has_errors = False

    def init_dict(self, key1: str, key2: str) -> Dict:
        return {key1: self.__getattribute__(key1), key2: self.__getattribute__(key2)}

    def set_values(self, data):
        self.email = data["email"]
        self.name = data["name"]
        self.username = data["username"]
        self.phone = data["phone"]

    def validate_email(self):
        validated_email = self.init_dict("email", "email_error")
        regrex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        match_re = re.compile(regrex)
        if not re.search(match_re, self.email):
            self.has_errors = True
            return {**validated_email, "email_error": "Email in not valid."}
        self.has_errors = False
        return validated_email

    def validate_phone(self):
        validated_phone = self.init_dict("phone", "phone_error")
        phone_reg = "^[6-9]\d{9}$"
        match_re = re.compile(phone_reg)
        res = re.search(match_re, self.phone)
        if not res:
            self.has_errors = True
            return {**validated_phone, "phone_error": "Phone number is invalid!"}

        return validated_phone

    def validate_name(self):
        validated_name = self.init_dict("name", "name_error")
        if len(self.name) < 3:
            self.has_errors = True
            return {**validated_name, "name_error": "Name is too short"}
        return validated_name

    def validate_username(self):
        validated_username = self.init_dict("username", "username_error")
        if len(self.username) < 3:
            self.has_errors = True
            return {
                **validated_username,
                "username_error": "Username name is too short",
            }
        return validated_username

    def validate_form_data(self):
        return {
            **self.validate_email(),
            **self.validate_phone(),
            **self.validate_name(),
            **self.validate_username(),
        }

    def create_user(self, form_data):
        self.set_values(form_data)
        d = self.validate_form_data()
        if not self.has_errors:
            user_exists = User.objects.filter(username=self.username).exists()
            if user_exists:
                return {**d, "username_error": "User Address already exists."}

            try:
                user = User.objects.create(
                    email=self.email, first_name=self.name, username=self.username
                )
                return user
            except Exception as e:
                print(e)
            except IntegrityError:
                return {**d, "username_error": "User already exists."}


def send_registration_confirm_mail(recipient_list: List, url):
    subject = "Welcome to MDRIFT! Confirm Your Email"
    html_content = get_template("registration-mail.html").render({"link": url})

    msg = EmailMessage(
        subject,
        html_content,
        config("EMAIL_HOST_USER"),
        recipient_list,
    )
    msg.content_subtype = "html"
    msg.send()


def get_permission_for_app(app_name):
    app = apps.get_app_config(app_name)
    all_permissions = []
    for model in app.get_models():
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        for p in permissions:
            all_permissions.append(p)
    return all_permissions
