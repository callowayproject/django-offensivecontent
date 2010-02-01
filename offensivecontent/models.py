from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
try:
    from core import logger
except:
    import logging as logger

class OffensiveContent(models.Model):
    """
    A way to retain data about Offensive User Content on the Site.
    """
    site = models.ForeignKey(Site)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    user = models.ForeignKey(User)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(auto_now_add=True)
    is_safe = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ("site", "content_type", "object_id", "user")

    def __unicode__(self):
        return unicode(self.get_content_instance())
    
    def get_absolute_url(self):
        return self.get_content_instance().get_absolute_url()

    def get_content_instance(self):
        """
        Shortcut to get the actual Instance of the piece of Content
        specified by content_type and object_id.
        """
        try:
            return self.content_type.get_object_for_this_type(pk=self.object_id)
        except self.content_type.DoesNotExist:
            logger.error("Offensive Content %d references a missing piece of content." % self.id)
            return None

    def view_content(self):
        """
        Returns link to view offensive content.
        """
        ci = self.get_content_instance()
        return '<a href="/admin/%s/%s/%d/">View Content</a>' % (ci._meta.app_label, ci._meta.module_name, ci.id)
    view_content.allow_tags = True
    view_content.is_safe = True
    
    def remove_content(self):
        """
        Returns link to remove offensive content.
        """
        return '<a href="/admin/offensivecontent/manage/remove_content/%d/">Remove Content</a>' % self.id
    remove_content.allow_tags = True
    remove_content.is_safe = True
    
    def remove_user_content(self):
        """
        Returns link to remove all user's submitted content.
        """
        return '<a href="/admin/offensivecontent/manage/remove_user_content/%d/">Remove User Content</a>' % self.id
    remove_user_content.allow_tags = True
    remove_user_content.is_safe = True
    
    def mark_content_safe(self):
        """
        Returns link to mark content as safe so other reports can not be filed.
        """
        return '<a href="/admin/offensivecontent/manage/mark_content_safe/%d/">Mark Content Safe</a>' % self.id
    mark_content_safe.allow_tags = True
    mark_content_safe.is_safe = True
    
    def disable_user(self):
        """
        Returns link to disable user and remove all user's submitted content.
        """
        return '<a href="/admin/offensivecontent/manage/disable_user/%d/">Disable User and Remove all User\'s Content</a>' % self.id
    disable_user.allow_tags = True
    disable_user.is_safe = True