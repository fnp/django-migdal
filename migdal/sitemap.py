# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.contrib.sitemaps import Sitemap
from django.utils.translation import override
from . import app_settings
from .models import Entry


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
for lc, ln in app_settings.LANGUAGES:
    sitemaps['entry_%s' % lc] = MigdalSitemap(lc)
