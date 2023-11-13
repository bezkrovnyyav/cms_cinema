from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'address',
                                                'language', 'gender', 'phone_number',
                                                'date_of_birth', 'number_card', 'town')}),
        ('Разрешения', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'username', 'first_name', 'last_name',
                    'email', 'is_staff', 'is_active', 'date_joined',
                    'address', 'language', 'gender', 'phone_number',
                    'date_of_birth', 'number_card', 'town')
    list_filter = ('is_staff', 'is_active', 'gender', 'town')
    list_display_links = ('id',)
    search_fields = ('username', 'email')


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ('id', 'town_name')
    list_display_links = ('id', 'town_name')
    search_fields = ('town_name',)
