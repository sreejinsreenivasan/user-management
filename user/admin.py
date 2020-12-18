from django.contrib import admin
from .models import Client, Country, Store, Image, User, UserProfile, Image
from django.contrib.auth.models import Group, Permission

admin.site.register(User)

admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Country)
admin.site.register(Store)
admin.site.register(Image)
admin.site.register(Permission)
