from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import UserSettings
from django.contrib.auth import get_user_model


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False
    fk_name = "user"


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
    inlines = (UserSettingsInline,)
    readonly_fields = ("id",)


admin.site.register(get_user_model(), CustomUserAdmin)
