from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user import models

admin.site.site_title = "Dona uz"
admin.site.site_header = "Dona uz"
admin.site.site_url = "https://dona.uz/"

admin.site.index_title = "Bosh sahifa"


admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ["firstname", "lastname", "phone_number", "region", "district"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                    "liked_products",
                    "firstname",
                    "lastname",
                    "region",
                    "district",
                )
            },
        ),
        # (_('Personal Info'),{'fields': ('id', )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": (
                    "firstname",
                    "lastname",
                    "phone_number",
                    "region",
                    "district",
                    "liked_products",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = (
        "phone_number",
        "firstname",
        "lastname",
        "region__name",
        "district__name",
    )
    ordering = ("phone_number",)


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ["contact", "code"]
    search_fields = ["contact"]


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "region"]
    search_fields = ["name", "region__name"]
