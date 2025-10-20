from django.contrib import admin
from .models import CustomUser,Profile
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# _______________________________________________________

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )
    
    list_display = ("email", "is_verified", "is_admin", "is_active")
    list_filter = ("email","is_active")
    search_fields = ("email",)
    ordering = ("created_date",)
    list_editable = ("is_active",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

admin.site.register(CustomUser,CustomUserAdmin)
# _______________________________________________________

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name','family','mobile_number','created_date')
    list_filter = ('mobile_number',)
    search_fields = ('family',)
    
admin.site.register(Profile,ProfileAdmin)
# _______________________________________________________
