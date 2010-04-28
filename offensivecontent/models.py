import datetime
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.http import urlquote

class OffensiveContent(models.Model):
    """
    A content object that has been marked as offensive
    """
    content_type = models.ForeignKey(ContentType, 
        verbose_name=_('Content Type'))
    object_id = models.IntegerField(_('Object ID'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    is_safe = models.NullBooleanField(_('Is Safe'), default=None, null=True,
        help_text=_('If True this peice of content has be verified not to be offensive.'))
    notes = models.TextField(_('Notes'), null=True, blank=True, 
        help_text=_('Some notes about this peice of content.'))
    site = models.ForeignKey(Site)
    latest = models.DateTimeField(auto_now=True)
    
    def moderator_actions(self):
        from django.contrib.auth import REDIRECT_FIELD_NAME
        STATIC_URL = getattr(settings, 'STATIC_URL', settings.MEDIA_URL)
        app_label = self.content_object._meta.app_label
        model = self.content_object._meta.module_name
        admin_url_name = 'admin:%s_%s_change' % (app_label, model)
        content_admin_url = reverse(admin_url_name, args=(self.object_id,))
        return_url = "?%s=%s" % (REDIRECT_FIELD_NAME, urlquote(reverse("admin:offensivecontent_offensivecontent_changelist")))
        return render_to_string('offensivecontent/admin/actions.html', {
            'object': self,
            'STATIC_URL': STATIC_URL,
            'content_admin_url': content_admin_url,
            'return_url': return_url,
        })
    moderator_actions.allow_tags = True
    
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
    