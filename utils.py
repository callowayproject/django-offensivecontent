from django.conf import settings
from ellington.weblogs.models import BANNED_DISPLAY_SETTING,Entry
from django.contrib.comments.models import Comment
from ellington.polls.models import Poll
#from users.settings import STATUS_BANNED as USER_STATUS_BANNED
#from community.settings import STATUS_BANNED as COMMUNITY_STATUS_BANNED
from community.models import CommunityUser
#from users.models import friendships
from django.contrib.auth.models import User

def get_user_from_content(content):
    """
    Gets the user from the content object.
    """
    if content.__class__ == Comment:
        return content.user
    elif content.__class__ == Entry:
        return content.author
    elif content.__class__ == User:
        return content
    elif content.__class__ == Poll:
        return # WTF?

def disable_content(content):
    """
    Disables the content.
    """
    if content.__class__ == Comment:
        content.is_removed = True
    elif content.__class__ == Entry:
        content.display = BANNED_DISPLAY_SETTING
    elif content.__class__ == CommunityUser:
        content.status = COMMUNITY_STATUS_BANNED
    elif content.__class__ == User:
        content.is_active = False
    content.save()

def remove_all_user_content(user):
    """
    Removes all user's content.
    """
    # Remove comments
    from django.contrib.auth.models import Group
    grp = Group.objects.get(pk=settings.COMMENTS_BANNED_USERS_GROUP)
    grp.user_set.add(user)
    
    # Remove weblog entries
    entry_list = user.get_weblogs_entry_list()
    for entry in entry_list:
        disable_content(entry)
    # Remove communities
    communityuser_list = user.get_community_communityuser_list()
    for communityuser in communityuser_list:
        disable_content(communityuser)
    # Remove friendships
    friendship_list = friendships.get_friendship_list(user.id)
    for friendship in friendship_list:
        friendship.update_user_status(user, USER_STATUS_BANNED)
        
def disable_user_instance(user):
    user.is_active = False
    user.save()