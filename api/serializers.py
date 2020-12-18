from rest_framework import serializers
from user.models import User, SignUpVerification, Client, Country, Store, UserProfile
from django.db import transaction
from django.contrib.auth.models import Group, Permission


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "username", "email", "permissions"]

    def get_permissions(self, obj):
        return obj.user_permissions.all().values()


class UpdateUserSerializer(serializers.Serializer):
    permissions = serializers.ListField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.email = validated_data.get("email", instance.email)
        permissions = validated_data.get("permissions")
        new_permissions = Permission.objects.filter(id__in=permissions)
        instance.user_permissions.add(*new_permissions)
        instance.save()
        return instance


class UserProfileSerailizer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_user(self, obj):
        user = User.objects.values("first_name", "email", "id").get(id=obj.user.id)
        return user

    def update(self, instance, validated_data):
        instance.user_type = validated_data.get("user_type", instance.user_type)
        instance.position = validated_data.get("position", instance.position)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.is_disabled = validated_data.get("is_disabled", instance.is_disabled)
        clients = validated_data.get("allowed_clients", None)
        countries = validated_data.get("allowed_countries", None)
        stores = validated_data.get("allowed_stores", None)

        if clients is not None:
            existing_clients = instance.allowed_clients["clients"]
            for i in clients:
                if not i in existing_clients:
                    existing_clients.append(i)
        if countries is not None:
            existing_countries = instance.allowed_countries["countries"]
            for i in countries:
                if not i in existing_countries:
                    existing_countries.append(i)
        if stores is not None:
            existing_stores = instance.allowed_stores["stores"]
            for i in stores:
                if not i in existing_stores:
                    existing_stores.append(i)
        instance.save()
        return instance


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
