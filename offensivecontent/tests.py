from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site

from models import OffensiveContent, OffensiveContentData

class TestOffensiveContent(TestCase):
    """Test of Offensive Content"""
    def setUp(self):
        self.offensive_user = User.objects.create_user('offensive_user', 'e@o.org', 'iamoffensive')
        self.offended_user = User.objects.create_user('offended_user', 'f@o.org', 'iamoffended')
        # add comment by offensive user
        self.comment = Comment.objects.create(user=self.offensive_user, comment='I hate you.', content_object=self.offended_user, site=Site.objects.get_current())
        # have offended user report it offensive
        self.offensive_content = OffensiveContent.objects.create(content_object=self.comment, site=Site.objects.get_current())
        oc_report = OffensiveContentData.objects.create(offensive_content=self.offensive_content, user=self.offended_user)

    def testDisableContent(self):
        pass
    
    def testEnableContent(self):
        pass
    
    def testDisableUser(self):
        pass
    
    def testEnableUser(self):
        pass
    
    def testModeratorActions(self):
        expected_html = '<a href="/admin/comments/comment/1/" target="_blank"><img src="/static/images/icons/page_magnify.png" title="View content" alt="View content" width="16" height="16"></a>\n<a href="/moderator/9/1/disable/"><img src="/static/images/icons/decline.png" title="Mark content as offensive" alt="Mark offensive" width="16" height="16"></a>\n<a href="/moderator/9/1/mark_safe/"><img src="/static/images/icons/accept.png" title="Mark content as safe" alt="Mark Safe" width="16" height="16"></a>\n<a href="/moderator/user/1/disable/"><img src="/static/images/icons/user_cross.png" title="Disable User" alt="Disable User" width="16" height="16"></a>\n'
        self.assertEqual(self.offensive_content.moderator_actions, expected_html)