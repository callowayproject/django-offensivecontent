from django.contrib.contenttypes.models import ContentType

class OffensiveContentController(object):
    """
    Default Controller, assumes active is the field for both
    the user field and content field and also assumes the types
    are Boolean.
    """
    user_field = 'active'
    content_field = 'active'
    content_user_field = 'user'
    
    user_field_disable_value = False
    content_field_disable_value = False
    user_field_enable_value = True
    content_field_enable_value = True
    
    def enable_user(self, instance):
        if hasattr(instance, self.content_user_field):
            attr = getattr(instance, self.content_user_field)
            if hasattr(attr, self.user_field):
                setattr(attr, self.user_field, self.content_field_enable_value)
                attr.save()
        
    def disable_user(self, instance):
        if hasattr(instance, self.content_user_field):
            attr = getattr(instance, self.content_user_field)
            if hasattr(attr, self.user_field):
                setattr(attr, self.user_field, self.user_field_disable_value)
                attr.save()
        
    def enable_content(self, instance):
        if hasattr(instance, self.content_field):
            setattr(instance, self.content_field, self.content_field_enable_value)
            instance.save()
        
    def disable_content(self, instance):
        if hasattr(instance, self.content_field):
            setattr(instance, self.content_field, self.content_field_disable_value)
            instance.save()
            
    def is_content_enabled(self, instance):
        if hasattr(instance, self.content_field):
            attr = getattr(instance, self.content_field) 
            if attr == self.content_field_enable_value:
                return True
            else:
                return False
        return None
        
    def is_content_user_enabled(self, instance):
        if hasattr(instance, self.content_user_field):
            attr = getattr(instance, self.content_user_field)
            if hasattr(attr, self.user_field):
                attr2 = getattr(attr, self.user_field)
                if attr2 == self.user_field_enable_value:
                    return True
                else:
                    return False
        return None
        
        
class ContentRegistry(object):
    def __init__(self):
        self._registry = {}
        
    def register(self, model, controller=OffensiveContentController):
        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            
        self._registry[model] = controller()

    def unregister(self, model):
        if model not in self._registry:
            raise NotRegistered('The model %s is not registered' % model.__name__)
        del self._registry[model]
        
    def is_registered(self, model):
        if model in self._registry:
            return True
        return False
        
    def get_controller_for_model(self, model):
        if model in self._registry:
            return self._registry[model]
        
        
registry = ContentRegistry()
