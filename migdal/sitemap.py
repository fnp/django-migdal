from django.contrib.sitemaps import Sitemap
from django.utils.translation import override
from .models import Entry
from django.conf import settings

class MigdalSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def __init__(self, lang):
        self.lang = lang

    def items(self):
        return Entry.objects.filter(**{"published_%s" % self.lang: True})

    def lastmod(self, obj):
        return obj.changed_at

    def location(self, obj):
        with override(self.lang):
            return obj.get_absolute_url()


sitemaps = {}
for lc, ln in settings.LANGUAGES:
    sitemaps['entry_%s' % lc] = MigdalSitemap(lc)
