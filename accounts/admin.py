from django.contrib import admin

from accounts.models import WebAuthDevice


@admin.register(WebAuthDevice)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ( 'user','name', 'credential_id', 'public_key','sign_count', 'transport', 'type', 'backed_up', 'created_at','updated_at', )
