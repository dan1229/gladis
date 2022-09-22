from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User
from django.contrib.auth import get_user_model



class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = (
        "is_active",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ) 
    list_display_links = (
        "is_active",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    ordering = []
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "password",
                    "last_login",
                    "is_staff",
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("id",)

admin.site.register(User, CustomUserAdmin)