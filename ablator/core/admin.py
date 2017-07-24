from django.contrib import admin

from core.models import ClientUser, FunctionalityGroup, Functionality, Availability


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)


@admin.register(FunctionalityGroup)
class FunctionalityGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)


@admin.register(Functionality)
class FunctionalityAdmin(admin.ModelAdmin):
    list_display = ('group', 'name', 'enable_probability', 'color', 'created_at',)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'functionality', 'created_at',)
