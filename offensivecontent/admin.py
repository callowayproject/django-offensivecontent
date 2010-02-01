from offensivecontent.models import OffensiveContent
from django.contrib import admin

class OffensiveContentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','is_safe','view_content','remove_content', 'remove_user_content', 'mark_content_safe', 'disable_user')
    raw_id_fields = ("user",)
admin.site.register(OffensiveContent, OffensiveContentAdmin)