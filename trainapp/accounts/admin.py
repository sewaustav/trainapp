from django.contrib import admin

from .models import JWTToken


# Register your models here.
@admin.register(JWTToken)
class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "expires_at")
    search_fields = ("user__email", "access_token")
    readonly_fields = ("access_token", "refresh_token", "created_at")