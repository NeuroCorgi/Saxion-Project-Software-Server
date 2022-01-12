from django.contrib import admin
from django.utils.html import format_html_join

from vault.models import Vault, OpeningLog

admin.site.register(OpeningLog)

@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
    
    @admin.display(description="Opening Log")
    def history(self, obj):
        return format_html_join("<br>", "{}, {}", ((log.time, log.success) for log in obj.history()))
