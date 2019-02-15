# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from migdal import feeds, app_settings
from migdal import views
from fnpdjango.utils.urls import i18n_patterns

pats = []
for t in app_settings.TYPES:
    pats += [
        # entry list
        url(string_concat(r'^', t.slug, r'/$'),
            views.entry_list, {'type_db': t.db},
            name='migdal_entry_list_%s' % t.db),
        url(string_concat(r'^', t.slug, r'/rss.xml$'),
            feeds.EntriesFeed(), {'type_db': t.db},
            name='migdal_entry_list_%s_feed' % t.db),
        # single entry
        url(string_concat(r'^', t.slug, r'/(?P<slug>[^/]+)/$'),
            views.entry, {'type_db': t.db},
            name='migdal_entry_%s' % t.db),
    ]


urlpatterns = i18n_patterns(
    # main page
    url(r'^$', views.main, name='migdal_main'),
    url(r'^rss.xml$', feeds.EntriesFeed(), name='migdal_main_feed'),
    # submit new entry
    url(string_concat(r'^', _('submit'), r'/$'), views.submit, name='migdal_submit'),
    url(string_concat(r'^', _('submit'), r'/', _('thanks'), r'$'), views.submit_thanks,
        name='migdal_submit_thanks'),
    # category
    url(string_concat(r'^', _('categories'), r'/(?P<category_slug>[^/]*)/$'),
        views.entry_list, name='migdal_category'),
    url(string_concat(r'^', _('categories'), r'/(?P<category_slug>[^/]*)/rss.xml$'),
        feeds.EntriesFeed(), name='migdal_category_feed'),
    url(string_concat(r'^', _('search')), views.SearchPublishedView(), name='search'),
    # type-specific views
    *pats
)


if 'django.contrib.sitemaps' in settings.INSTALLED_APPS:
    import django.contrib.sitemaps.views
    from .sitemap import sitemaps
    urlpatterns += (
        url(r'^sitemap\.xml$', django.contrib.sitemaps.views.sitemap, {
            'sitemaps': sitemaps
        }),
    )
