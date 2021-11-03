from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    """
    Render the homepage template.

    * Only authenticated users can access to the homepage.
    """

    def get_template_names(self):
        if settings.DEBUG:
            template_name = 'index.html'
        else:
            template_name = 'index.html'
        return template_name
