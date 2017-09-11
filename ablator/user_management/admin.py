from django.contrib import admin

from user_management.models import AblatorUser, Organization


@admin.register(AblatorUser)
class AblatorUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
