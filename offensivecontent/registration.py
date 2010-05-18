from controllers import OffensiveContentController

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class ControllerNotFound(Exception):
    pass

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
        else:
            raise ControllerNotFound("Couldn't find a controller for %s in (%s)" % (model, self._registry.keys()))
        
        
registry = ContentRegistry()

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.importlib import import_module

DEFAULT_REGISTRY = getattr(settings, "OCONTENT_REGISTRY", [])

# The default registry is a list of tuples of strings
# [('app.model','app.module.ControllerClass'),]
for model, controller_class in DEFAULT_REGISTRY:
    app_label, model_name = model.split('.')
    ctype = ContentType.objects.get(app_label=app_label, model=model_name)
    module_array = controller_class.split(".")
    ctrlr_module = import_module(".".join(module_array[0:-1]))
    ctrlr = getattr(ctrlr_module, module_array[-1])
    registry.register(ctype.model_class(), ctrlr)
