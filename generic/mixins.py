from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin


class UserIsOwnerOrAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (request.user == obj.user or request.user.is_superuser or request.user.isSecretary):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

