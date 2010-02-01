import unittest
from offensivecontent.utils import get_user_from_content, remove_all_user_content, disable_user_instance, disable_content
from django.contrib.auth.models import User
from django.conf import settings
from ellington.weblogs.models import BANNED_DISPLAY_SETTING, Entry
#from users.settings import STATUS_BANNED as USER_STATUS_BANNED
#from community.settings import STATUS_BANNED as COMMUNITY_STATUS_BANNED
from threadedcomments.models import ThreadedComment

class TestOffensiveContent(unittest.TestCase):
    """
    This TestCase exercises Offensive Content.
    """

    def setUp(self):
        self.user_iterator = users.get_iterator()
        self.user = self.user_iterator.next()
        while not len(self.user.get_comments_comment_list()) > 0 or not len(self.user.get_weblogs_entry_list()) > 0:
            self.user = self.user_iterator.next()
        self.comment = comments.get_iterator().next()
        self.entry = entries.get_iterator().next()
                
    def test_data(self):
        """
        Makes sure there is data to test.
        """
        self.assert_(not self.user == None)
        self.assert_(not self.comment == None)
        self.assert_(not self.entry == None)

    def test_disable_content_comment(self):
        """
        Makes sure disable_content for a Comment works.
        """
        if self.comment.is_removed:
            self.comment.is_removed = False
            self.comment.save()
            disable_content(self.comment)
            self.assert_(self.comment.is_removed)
        else:
            disable_content(self.comment)
            self.assert_(self.comment.is_removed)
            self.comment.is_removed = False
            self.comment.save()

    def test_disable_content_user(self):
        """
        Makes sure disable_content for a User works.
        """
        if self.user.is_active:
            disable_content(self.user)
            self.assert_(not self.user.is_active)
            self.user.is_active = True
            self.user.save()
            self.assert_(self.user.is_active)
        else:
            self.user.is_active = True
            self.user.save()
            disable_content(self.user)
            self.assert_(not self.user.is_active)

    def test_get_user_from_content(self):
        """
        Makes sure the user returned is the actual owner of the content queried.
        """
        self.assertEqual(get_user_from_content(self.comment), self.comment.get_user())
        self.assertEqual(get_user_from_content(self.entry), self.entry.get_author())

    def test_remove_all_user_content(self):
        """
        Makes sure remove all user content disables all content appropriately.
        """
        remove_all_user_content(self.user)
        self.assert_(settings.COMMENTS_BANNED_USERS_GROUP in [g.id for g in self.user.get_group_list()])
        entry_list = self.user.get_weblogs_entry_list()
        for entry in entry_list:
            self.assertEqual(entry.display, BANNED_DISPLAY_SETTING)
        communityuser_list = self.user.get_community_communityuser_list()
        for communityuser in communityuser_list:
            self.assertEqual(communityuser.status, COMMUNITY_STATUS_BANNED)
        friendship_list = friendships.get_friendship_list(self.user.id)
        for friendship in friendship_list:
            if friendship.get_to_user() == self.user:
                self.assertEqual(friendship.to_status, USER_STATUS_BANNED)
            else:
                self.assertEqual(friendship.from_status, USER_STATUS_BANNED)
    
    def test_disable_user(self):
        """
        Makes sure disable_user deactivates a user appropriately.
        """
        if self.user.is_active:
            disable_user_instance(self.user)
            self.assert_(not self.user.is_active)
            self.user.is_active = True
            self.user.save()
        else:
            self.user.is_active = True
            self.user.save()
            disable_user_instance(self.user)
            self.assert_(not self.user.is_active)