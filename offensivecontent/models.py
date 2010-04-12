import datetime, random
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.core.cache import cache
from django.conf import settings

class OffensiveContent(models.Model):
    """
    A content object that has been marked as offensive
    """
    content_type = models.ForeignKey(ContentType, 
        verbose_name=_('Content Type'))
    object_id = models.IntegerField(_('Object ID'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    is_safe = models.BooleanField(_('Is Safe'), default=False, 
        help_text=_('If True this peice of content has be verified not to be offensive.'))
    notes = models.TextField(_('Notes'), null=True, blank=True, 
        help_text=_('Some notes about this peice of content.'))
    site = models.ForeignKey(Site)
    latest = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("site", "content_type", "object_id",)
        ordering = ('-latest',)

    def __unicode__(self):
        return unicode(self.content_object)
        
    
class OffensiveContentData(models.Model):
    """
    Information about the user that marked content as offensive
    """
    offensive_content = models.ForeignKey(OffensiveContent)
    user = models.ForeignKey(User)
    comment = models.TextField(blank=True, null=True)
    pub_date = models.DateField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return "%s - %s" % (self.offensive_content, self.user)
        
    class Meta:
        ordering = ('-pub_date',)
    