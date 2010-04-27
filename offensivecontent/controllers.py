class OffensiveContentController(object):
    """
    Default Controller, assumes active is the field for both
    the user field and content field and also assumes the types
    are Boolean.
    """
    user_field = 'is_active'
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

class OffensiveCommentController(OffensiveContentController):
    content_field = 'is_public'

