from django.conf import settings
from django.db import models
from django_hosts.resolvers import reverse

from .utils import create_shortcode
from .validators import validate_url

# Create your models here.


SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)


class deepURLManager(models.Manager):
    def refresh_allcode(self):
        qs = deepURL.objects.filter(id__gte=1)
        newcodes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.shortcode)
            q.save()
            newcodes += 1
        return "NewCodes Made: {i}".format(i=newcodes)


class deepURL(models.Model):
    url = models.CharField(max_length=254, validators=[validate_url])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True)
    fallback_url = models.CharField(max_length=254, validators=[validate_url], blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = deepURLManager()

    def __str__(self):
        return str(self.shortcode)

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        super(deepURL, self).save(*args, **kwargs)

    def small_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='127', scheme='http')
        return url_path
