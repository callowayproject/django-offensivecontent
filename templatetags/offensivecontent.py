from django import template
from django.contrib.contenttypes.models import ContentType
from offensivecontent.models import OffensiveContent
from ellington.core.parts.templatetags import CachedContextUpdatingNode

register = template.Library()

class OffensiveContentLinkNode(CachedContextUpdatingNode):
    """
    Gets Offensive Content Link for object.
    """
    def __init__(self, obj, varname):
        self.obj = obj
        self.varname = varname

    def get_cache_key(self, context):
        from ellington.core.utils import get_cache_prefix
        obj = str(template.resolve_variable(self.obj, context))
        return 'coltrane.offensivecontent.templatetags.get_offensive_content_link_url:%s:%s' % (obj, get_cache_prefix())
        
    def get_content(self, context):
        obj = template.resolve_variable(self.obj, context)
        contenttype = ContentType.objects.get_for_model(obj.__class__)
        off_cont = OffensiveContent.objects.filter(object_id__exact=obj.id, 
                                              content_type__id__exact=contenttype.id)
        if off_cont:
            link_url = False
        else:
            link_url = "/offensivecontent/add/%d/%d/" % (contenttype.id, obj.id)
        return {self.varname: link_url}
    
def get_offensive_content_link_url(parser, token):
    """
    {% get_offensive_content_link_url for object as link_url %}
    """
    bits = token.contents.split()
    if len(bits) < 5:
        raise template.TemplateSyntaxError, "%r tag requires at least four argument" % bits[0]
    if bits[1] != 'for':
        raise template.TemplateSyntaxError, "first argument to the %r tag must be 'for'" % bits[0]
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "third argument to the %r tag must be 'as'" % bits[0]
    return OffensiveContentLinkNode(bits[2], bits[4])

register.tag("get_offensive_content_link_url", get_offensive_content_link_url)