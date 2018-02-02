from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import deepURL


class RedirectUrl(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(deepURL, shortcode=shortcode)
        qs = deepURL.objects.filter(shortcode=shortcode)
        if qs.exists():
            obj = qs.first()
            context = {'url': obj.url}
            template = "shortener/jump.html"
            return render(request, template, context)
        return Http404
