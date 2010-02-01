from django.dispatch import dispatcher
from django.core import signals
from offensivecontent.models import OffensiveContent

def remove_safe_check(signal, sender, instance):
    """
    Marks this content as not safe anymore as it has been edited.
    """
    if hasattr(instance, instance._models.pk.name):
        try:
            object_id = int(getattr(instance, instance._models.pk.name))
            offensivecontent = OffensiveContent.objects.get(content_type__id=instance._models.get_content_type_id(), object_id=object_id)
            offensivecontent.is_safe = False
            offensivecontent.save()
        except (OffensiveContent.DoesNotExist, ValueError):
            pass
dispatcher.connect(remove_safe_check, signal=signals.post_save)

def delete_offensive_content(signal, sender, instance):
    """
    Deletes OffensiveContent when the content referenced is deleted.
    """
    if hasattr(instance, instance._models.pk.name):    
        try:
            object_id = int(getattr(instance, instance._models.pk.name))
            offensivecontent = OffensiveContent.objects.get(content_type__id=instance._models.get_content_type_id(), object_id=object_id)
            offensivecontent.delete()
        except (OffensiveContent.DoesNotExist, ValueError):
            pass
dispatcher.connect(delete_offensive_content, signal=signals.pre_delete)