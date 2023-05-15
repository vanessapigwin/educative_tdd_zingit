from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Song, Playlist, CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'full_name'
    )
    

# Register your models here.
admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(CustomUser, CustomUserAdmin)