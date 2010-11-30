from django.contrib import admin
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from offensivecontent.models import OffensiveContent, OffensiveContentData
try:
    from offensivecontent import registry
except ImportError:
    from registration import registry

def _do_action(modeladmin, request, queryset, method):
    for oc in queryset:
        controller = registry.get_controller_for_model(
            oc.content_type.model_class())
        getattr(controller, method)(oc.content_type.get_object_for_this_type(pk=oc.object_id))
    return len(queryset)
    
def _get_message(rows_updated, app_text, app_text_plural, result_text):
    if rows_updated == 1:
        message_bit = "1 %s was" % app_text
    else:
        message_bit = "%s %s were" % (rows_updated, app_text_plural)
    return "%s sucessfully %s" % (message_bit, result_text)
    
class OffensiveContentDataInline(admin.TabularInline):
    model = OffensiveContentData
    raw_id_fields = ('user',)
    

class OffensiveContentAdmin(admin.ModelAdmin):
    list_display = ('get_content_text', 'is_safe', 'number_of_submitters', 'latest', 'moderator_actions')
    inlines = [OffensiveContentDataInline,]
    actions = ['disable_content', 'enable_content', 'disable_user', 
        'enable_user', 'mark_safe', 'mark_unsafe']
    date_hierarchy = "latest"
    list_filter = ["is_safe","content_type"]
    actions_on_bottom = True
    
    def get_content_text(self, obj):
        if isinstance(obj.content_object, Comment):
            return "%s: %s" % (obj.content_object.name, obj.content_object.comment)
        return obj.content_object
    get_content_text.short_description = "Content Text"
    
    def number_of_submitters(self, obj):
        return str(OffensiveContentData.objects.filter(offensive_content__pk=obj.pk).count())
    number_of_submitters.short_description = "Num. Of Marks"
    
    def is_content_enabled(self, obj):
        controller = registry.get_controller_for_model(obj.content_type.model_class())
        return controller.is_content_enabled(obj.content_type.get_object_for_this_type(pk=obj.object_id))
    is_content_enabled.short_description = "Is Content Enabled"
    
    def is_content_user_enabled(self, obj):
        controller = registry.get_controller_for_model(obj.content_type.model_class())
        return controller.is_content_user_enabled(obj.content_type.get_object_for_this_type(pk=obj.object_id))
    is_content_user_enabled.short_description = "Is Content User Enabled"
        
    def disable_content(self, request, queryset):
        rows_updated = _do_action(self, request, queryset, 'disable_content')
        self.message_user(
            request, _get_message(
                rows_updated, 'content', 'contents', 'disabled'))
    disable_content.short_description = "Disable selected content."
    
    def enable_content(self, request, queryset):
        rows_updated = _do_action(self, request, queryset, 'enable_content')
        self.message_user(
            request, _get_message(
                rows_updated, 'content', 'contents', 'enabled'))
    enable_content.short_description = "Enable selected content."
    
    def disable_user(self, request, queryset):
        rows_updated = _do_action(self, request, queryset, 'disable_user')
        self.message_user(
            request, _get_message(
                rows_updated, 'content user', 'content users', 'disabled'))
    disable_user.short_description = "Disable selected content user."
    
    def enable_user(self, request, queryset):
        rows_updated = _do_action(self, request, queryset, 'enable_user')
        self.message_user(
            request, _get_message(
                rows_updated, 'content user', 'content users', 'enabled'))
    enable_user.short_description = "Enable selected content user."
    
    def mark_safe(self, request, queryset):
        rows_updated = queryset.update(is_safe=True)
        _do_action(self, request, queryset, 'enable_content')
        self.message_user(
            request, _get_message(
                rows_updated, 'content', 'contents', 'marked safe'))
    mark_safe.short_description = "Mark selected content safe."
    
    def mark_unsafe(self, request, queryset):
        rows_updated = queryset.update(is_safe=False)
        _do_action(self, request, queryset, 'disable_content')
        self.message_user(
            request, _get_message(
                rows_updated, 'content', 'contents', 'marked unsafe'))
    mark_unsafe.short_description = "Mark selected content unsafe."
    
    
class OffensiveContentDataAdmin(admin.ModelAdmin):
    list_display = ('content_label', 'user', 'comment', 'pub_date',)
    raw_id_fields = ('user',)
    
    def content_label(self, obj):
        return "%s (%s)" % (str(obj.offensive_content), str(obj.offensive_content.content_type))
    content_label.short_description = "Content"
    
    
admin.site.register(OffensiveContent, OffensiveContentAdmin)
admin.site.register(OffensiveContentData, OffensiveContentDataAdmin)