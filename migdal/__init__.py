# -*- coding: utf-8 -*-
"""
Migdal (מִגְדָּל) is a multilingual blog Django app.

Author: Radek Czajka <radoslaw.czajka@nowoczesnapolska.org.pl>
"""
from django.conf import settings
from fnpdjango.utils.app import AppSettings
from django.utils.translation import ugettext_lazy as _
from migdal.helpers import EntryType


class Settings(AppSettings):
    # Types of entries:
    # (slug, commentable, on main)
    TYPES = (
            EntryType('news', _('news'), commentable=True, on_main=True, promotable=True),
            EntryType('publications', _('publications')),
            EntryType('info', _('info')),
            EntryType('event', _('events')),
        )
    TYPE_SUBMIT = 'news'
    TAXONOMIES = (
        ('topics', _('topics')),
        ('types', _('types')),
    )
    LAST_COMMENTS = 5

    MAIN_PAGE_ENTRY = None

    def _more_TYPES_DICT(self, value):
        return dict((t.db, t) for t in self.TYPES)
    TYPES_DICT = None

    def _more_TYPES_ON_MAIN(self, value):
        return tuple(t.db for t in self.TYPES if t.on_main)
    TYPES_ON_MAIN = None

    def _more_TYPES_PROMOTABLE(self, value):
        return tuple(t.db for t in self.TYPES if t.promotable)
    TYPES_PROMOTABLE = None

    def _more_OBLIGATORY_LANGUAGES(self, value):
        return value or tuple(lang for lang in settings.LANGUAGES if lang[0] == settings.LANGUAGE_CODE)
    OBLIGATORY_LANGUAGES = None

    def _more_OPTIONAL_LANGUAGES(self, value):
        if value is None:
            return tuple(lang for lang in settings.LANGUAGES if lang not in self.OBLIGATORY_LANGUAGES)
        else:
            return value
    OPTIONAL_LANGUAGES = None

    def _more_LANGUAGES(self, value):
        return self.OBLIGATORY_LANGUAGES + self.OPTIONAL_LANGUAGES
    LANGUAGES = None

    PUBLISH_DATE_EDITABLE = False

app_settings = Settings('MIGDAL')
