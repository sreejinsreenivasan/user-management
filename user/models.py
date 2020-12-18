from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    is_active = models.BooleanField(default=False)


class UserProfile(models.Model):
    TYPE_CHOICES = [("STAFF", "Staff"), ("CLIENT", "Client")]
    user = models.OneToOneField(
        "user.User", related_name="profile", on_delete=models.CASCADE
    )

    uid = models.UUIDField(default=uuid.uuid4())
    user_type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    position = models.CharField(max_length=99)
    phone_number = models.CharField(max_length=12)
    allowed_clients = models.JSONField(default=dict)
    allowed_countries = models.JSONField(default=dict)
    allowed_stores = models.JSONField(default=dict)
    email_notification = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "user.User", related_name="created_profiles", on_delete=models.DO_NOTHING
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        "user.User", related_name="modified_profiles", on_delete=models.DO_NOTHING
    )


class Image(models.Model):
    user = models.OneToOneField(
        "user.User", related_name="profile_image", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="images/%d%m/%y")


class Permission(models.Model):
    name = models.CharField(max_length=250)
    # index = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "user.User", related_name="created_permissions", on_delete=models.DO_NOTHING
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        "user.User", related_name="modified_permissions", on_delete=models.DO_NOTHING
    )


class Client(models.Model):
    name = models.CharField(max_length=250)
    uid = models.UUIDField(default=uuid.uuid4())
    is_disabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "user.User", related_name="created_clients", on_delete=models.DO_NOTHING
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        "user.User", related_name="modified_clients", on_delete=models.DO_NOTHING
    )


class Country(models.Model):
    name = models.CharField(max_length=250)
    flag = models.ImageField(upload_to="flags")
    currency_name = models.CharField(max_length=250)
    currency_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "user.User", related_name="created_countries", on_delete=models.DO_NOTHING
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        "user.User", related_name="modified_countries", on_delete=models.DO_NOTHING
    )


class Store(models.Model):
    uid = models.UUIDField(default=uuid.uuid4())
    client = models.ForeignKey(
        "user.Client", related_name="stores", on_delete=models.CASCADE
    )
    country = models.ForeignKey(
        "user.Country", related_name="stores", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)


class SignUpVerification(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4())