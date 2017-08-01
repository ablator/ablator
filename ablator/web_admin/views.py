from django.shortcuts import render
from django.views.generic.base import TemplateView

from core.models import App


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['apps'] = App.objects.all()
        return context_data
