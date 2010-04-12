from django.conf.urls.defaults import *

urlpatterns = patterns('offensivecontent.views',
    (r'^add/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 'add'),
    
    (r'^disable_content/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 
        'content_cotroller', {'method': 'disable_content'}),
        
    (r'^enable_content/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 
        'content_cotroller', {'method': 'enable_content'}),
        
    (r'^disable_user/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 
        'content_cotroller', {'method': 'disable_user'}),
        
    (r'^enable_user/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 
        'content_cotroller', {'method': 'enable_user'}),

    (r'^mark_safe/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$', 'mark_safe')
)