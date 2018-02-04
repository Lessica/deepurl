import urllib
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
            get_args = urllib.urlencode(request.GET)
            url = obj.url
            if len(get_args) > 0:
                url = obj.url + '?' + get_args
            context = {'url': url, 'fallback_url': obj.fallback_url}
            template = "shortener/jump.html"
            return render(request, template, context)
        return Http404
