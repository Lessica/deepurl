import urllib
import json

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import deepURL


class RedirectUrl(View):
    cache_timeout = 0

    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(deepURL, shortcode=shortcode)
        qs = deepURL.objects.filter(shortcode=shortcode)
        if qs.exists():
            obj = qs.first()
            get_args = request.GET.copy()
            get_args.pop('_json', None)
            jump_url = obj.url
            if len(get_args) > 0:
                jump_url = obj.url + '?' + get_args.urlencode()
            context = {'shortcode': shortcode, 'jump_url': jump_url, 'fallback_url': obj.fallback_url}
            if '_json' in request.GET:
                return HttpResponse(json.dumps(context), content_type="application/json")
            template = "shortener/jump.html"
            return render(request, template, context)
        return Http404
