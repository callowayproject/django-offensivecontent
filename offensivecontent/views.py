from django.views.generic.create_update import create_object
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 
from django.conf import settings
from offensivecontent.models import OffensiveContent
from offensivecontent.utils import get_user_from_content, disable_content, remove_all_user_content, disable_user_instance
from django.http import HttpResponseRedirect,Http404

def add(request, content_type_id, object_id):
    """
    Adds content as offensive.
    """
    contenttype = get_object_or_404(ContentType, pk=content_type_id)
    try:
        content = contenttype.get_object_for_this_type(pk=object_id)
    except OffensiveContent.DoesNotExist:
        raise Http404
    try:
        offensivecontent = OffensiveContent.objects.filter(content_type__id=content_type_id, object_id=object_id)[0]
        if offensivecontent.is_safe:
            message = "This content has been marked as safe."
            return render_to_response('offensivecontents_form.html', {'message': message, 'content': content}, RequestContext(request))
    except (OffensiveContent.DoesNotExist, IndexError):
        pass
    try:
        offensivecontent = OffensiveContent.objects.get(user__id=request.user.id, content_type__id=content_type_id, object_id=object_id)
        message = "You have already marked this content as offensive."
        return render_to_response('offensivecontents_form.html', {'message': message, 'content': content}, RequestContext(request))
    except OffensiveContent.DoesNotExist:
        pass
    return create_object(request, OffensiveContent, 'offensivecontents_form.html', post_save_redirect=content.get_absolute_url(), extra_context={'site_id': settings.SITE_ID, 'content_type_id': content_type_id, 'object_id': object_id, 'content': content,}, login_required=True)
add = login_required(add)

def remove_content(request, offensive_content_id):
    """
    Removes offensive content.
    """
    offensivecontent = get_object_or_404(OffensiveContent, pk=offensive_content_id)
    content = offensivecontent.get_content_instance()
    if content:
        disable_content(content)
    return HttpResponseRedirect('/admin/%s/%s/' % (OffensiveContent._models.app_label, OffensiveContent._models.module_name))
remove_content = staff_member_required(remove_content)

def remove_user_content(request, offensive_content_id):
    """
    Removes user's submitted content.
    """
    offensivecontent = get_object_or_404(OffensiveContent, pk=offensive_content_id)
    content = offensivecontent.get_content_instance()
    if content:
        remove_all_user_content(get_user_from_content(content))
    return HttpResponseRedirect('/admin/%s/%s/' % (OffensiveContent._models.app_label, OffensiveContent._models.module_name))
remove_user_content = staff_member_required(remove_user_content)

def mark_content_safe(request, offensive_content_id):
    """
    Marks content as safe so that other reports do not get processed.
    """
    offensivecontent = get_object_or_404(OffensiveContent, id__exact=offensive_content_id)
    offensivecontent.is_safe = True
    offensivecontent.save()
    return HttpResponseRedirect('/admin/%s/%s/' % (OffensiveContent._models.app_label, OffensiveContent._models.module_name))
mark_content_safe = staff_member_required(mark_content_safe)

def disable_user(request, offensive_content_id):
    """
    Disables user and removes their submitted content.
    """
    offensivecontent = get_object_or_404(OffensiveContent, id__exact=offensive_content_id)
    content = offensivecontent.get_content_instance()
    if content:
        user = get_user_from_content(content)
        disable_user_instance(user)
    return remove_user_content(request, offensive_content_id)
disable_user = staff_member_required(disable_user)