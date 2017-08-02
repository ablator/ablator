from django.contrib import admin

from core.models import Release
from .models import ClientUser, Functionality, Flavor, Availability, App


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('human_readable_name', 'name', 'created_at',)


class FunctionalityInline(admin.TabularInline):
    model = Flavor


@admin.register(Functionality)
class FunctionalityGroupAdmin(admin.ModelAdmin):
    list_display = ('human_readable_name', 'name', 'app', 'created_at', 'rollout_strategy')
    inlines = [FunctionalityInline]


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'functionality',
        'start_at',
        'end_at',
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'flavor', 'is_enabled', 'created_at',)
