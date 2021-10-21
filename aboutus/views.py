from django.views.generic import TemplateView  # Importing template class based views


class AboutUsView(TemplateView):  # Initializing template for template view
    template_name = 'about/about.html'
