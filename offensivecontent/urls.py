from django.conf.urls.defaults import *
from django.contrib.contenttypes.models import ContentType

user_contenttype_id = ContentType.objects.get(app_label='auth', name='user')

urlpatterns = patterns('offensivecontent.views',
    url(
        regex = r'^(?P<content_type_id>\d+)/(?P<object_id>\d+)/add/$', 
        view = 'add',
        name = 'oc_add',
    ),
    url(
        regex = r'^(?P<content_type_id>\d+)/(?P<object_id>\d+)/add_ajax/$', 
        view = 'add_ajax',
        name = 'oc_add_ajax',
    ),
    url(
        regex = r'^(?P<object_id>\d+)/disable/$', 
        view = 'content_cotroller', 
        kwargs = {'method': 'disable_content'},
        name = 'oc_disable_content'
    ),
    url(
        regex = r'^(?P<object_id>\d+)/enable/$', 
        view = 'content_cotroller', 
        kwargs = {'method': 'enable_content'},
        name = 'oc_enable_content',
    ),
    url(
        regex = r'^user/(?P<object_id>\d+)/disable/$', 
        view = 'content_cotroller', 
        kwargs = {
            'content_type_id': user_contenttype_id, 
            'method': 'disable_user'},
        name = "oc_disable_user"
    ),
    url(
        regex = r'^user/(?P<object_id>\d+)/enable/$', 
        view = 'content_cotroller', 
        kwargs = {
            'content_type_id': user_contenttype_id, 
            'method': 'enable_user'},
        name = "oc_enable_user"
    ),
    url(
        regex = r'^(?P<object_id>\d+)/mark_safe/$', 
        view = 'mark_safe',
        kwargs = {'is_safe': True,},
        name = "oc_mark_safe",
    ),
)