from django.contrib import admin

from core.models import RolloutStrategy
from .models import ClientUser, Functionality, Flavor, Availability, App


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name",
        "created_at",
    )
    prepopulated_fields = {"slug": ("name",)}


class FlavorInline(admin.TabularInline):
    model = Flavor
    readonly_fields = ("id",)


class ReleaseInline(admin.TabularInline):
    model = RolloutStrategy
    readonly_fields = ("id",)


@admin.register(Functionality)
class FunctionalityAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "app", "created_at")
    inlines = [FlavorInline, ReleaseInline]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id",)


@admin.register(RolloutStrategy)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "functionality",
        "start_at",
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "flavor",
        "is_enabled",
        "created_at",
    )
    readonly_fields = ("user", "flavor", "created_at")
