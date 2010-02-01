from django.conf.urls.defaults import *

urlpatterns = patterns('offensivecontent.views',
    (r'^add/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 'add'),

    #admin
    (r'^remove_content/(?P<offensive_content_id>\d+)/$', 'remove_content'),
    (r'^remove_user_content/(?P<offensive_content_id>\d+)/$', 'remove_user_content'),
    (r'^mark_content_safe/(?P<offensive_content_id>\d+)/$', 'mark_content_safe'),
    (r'^disable_user/(?P<offensive_content_id>\d+)/$', 'disable_user'),
)