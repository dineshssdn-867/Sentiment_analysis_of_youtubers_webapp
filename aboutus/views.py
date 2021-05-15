from django.views.generic import TemplateView  # Importing template class based views
from sentiment.views import CacheMixin # this library is used for caching


class AboutUsView(TemplateView, CacheMixin):  # Initializing template for template view
    template_name = 'about/about.html'
