from django.views.generic.create_update import create_object
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.admin.views.decorators import staff_member_required 
from django.conf import settings
from django.http import HttpResponseRedirect, Http404

from offensivecontent import registry
from offensivecontent.models import OffensiveContent, OffensiveContentData
from offensivecontent.forms import MarkForm

def _user_has_marked(user, content_type_id, object_id):
    try:
        OffensiveContentData.objects.get(
            user__pk=user.pk,
            offensive_content__content_type__pk=content_type_id,
            offensive_content__object_id=object_id)
        return True
    except OffensiveContentData.DoesNotExist, OffensiveContentData.MultipleObjectsReturned:
        return False

@login_required
def add(request, content_type_id, object_id, 
    template_name="offensivecontent/form.html"):
        
    return_url = '/'
    if 'ret' in request.GET:
        return_url = request.GET['ret']
        
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    site = get_object_or_404(Site, pk=settings.SITE_ID)
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
        
    if not registry.is_registered(ctype.model_class()):
        raise Http404
    
    if request.method == "POST":
        if _user_has_marked(request.user, content_type_id, object_id):
            return HttpResponseRedirect(return_url)
            
        form = MarkForm(request.POST)
        if form.is_valid():
            oc, created = OffensiveContent.objects.get_or_create(
                content_type=ctype, object_id=object_id, site=site)
            
            data = form.save(commit=False)
            data.user = request.user
            data.offensive_content = oc
            data.save()
            
            return HttpResponseRedirect(return_url)
    else:
        form = MarkForm()
        
    return render_to_response(template_name,
                              {'form': form, 
                               'obj': obj,
                               'ctype': ctype,
                               'return_url': return_url},
                              context_instance=RequestContext(request))


@staff_member_required
def mark_safe(request, content_type_id, object_id, is_safe=False
    template_name='offensivecontent/admin/confirm_form.html'):
    
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    oc = get_object_or_404(OffensiveContent, 
        content_type__pk=content_type_id,
        object_id=object_id)
    
    if request.method == "POST":
        if "confirm" in request.POST:
            controller = registry.get_controller_for_model(ctype.model_class())
            controller.enable_content(ctype.get_object_for_this_type(pk=object_id))
            oc.is_safe = True
            oc.save()
            
    return render_to_response(template_name,
                              {'ctype': ctype,
                               'obj': obj},
                              context_instance=RequestContext(request))

MESSAGES = {
    'disable_user': "Are you sure you want to disable the user for this content?",
    'enable_user': "Are you sure you want to enable the user for this content?",
    'disable_content': "Are you sure you want to disable this content?",
    'enable_content': "Are you sure you want to enable this content?"
}

@staff_member_required
def content_cotroller(request, content_type_id, object_id, 
    template_name="offensivecontent/admin/confirm_form.html", method=None):
    
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    
    try:
        ctype = ContentType.objects.get(pk=content_type_id)
    except ContentType.DoesNotExist:
        raise Http404
        
    if request.method == "POST":
        if "confirm" in request.POST:
            controller = registry.get_controller_for_model(ctype.model_class())
            getattr(controller, method)(ctype.get_object_for_this_type(pk=object_id))
            # TODO reirect
            
    return render_to_response(template_name,
                              {'ctype': ctype,
                               'obj': obj,
                               'message': MESSAGES[method]},
                              context_instance=RequestContext(request))
                              