from django.contrib import admin

from user_management.models import AblatorUser, Company


@admin.register(AblatorUser)
class AblatorUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
