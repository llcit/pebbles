from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core import management
from django.contrib import messages

class UpdateIndexView(TemplateView):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        management.call_command('update_index')
        messages.info(request, 'Index has been updated.')
        return redirect('haystack_search')
