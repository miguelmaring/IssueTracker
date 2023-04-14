from django.contrib import admin
from users.models import User, Log
# Register your models here.
"""
class LogsInline(admin.TabularInline):
    model = Log


class UserAdmin(admin.ModelAdmin):
    inlines = [
        LogsInline,
    ]


admin.site.register(User, UserAdmin)
"""

admin.site.register(User)
admin.site.register(Log)