# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers, send_mail
from django.db import models
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _, ugettext
from django_comments_xtd.models import XtdComment
from fnpdjango.utils.fields import TextileField
from fnpdjango.utils.models.translation import add_translatable, tQ
from migdal import app_settings
from migdal.fields import SlugNullField


class Category(models.Model):
    taxonomy = models.CharField(_('taxonomy'), max_length=32, choices=app_settings.TAXONOMIES)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.title or u""

    @models.permalink
    def get_absolute_url(self):
        return 'migdal_category', [self.slug]


add_translatable(Category, {
    'title': models.CharField(max_length=64, unique=True, db_index=True),
    'slug': models.SlugField(unique=True, db_index=True),
})


class PublishedEntryManager(models.Manager):
    def get_query_set(self):
        return super(PublishedEntryManager, self).get_query_set().filter(
                tQ(published=True)
            )


class PhotoGallery(models.Model):
    key = models.CharField(max_length=64)

    def __unicode__(self):
        return self.key


class Photo(models.Model):
    gallery = models.ForeignKey(PhotoGallery)
    image = models.ImageField(_('image'), upload_to='entry/photo/', null=True, blank=True)


class Entry(models.Model):
    type = models.CharField(
        max_length=16,
        choices=((t.db, t.slug) for t in app_settings.TYPES),
        db_index=True)
    date = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(_('changed at'), auto_now=True, db_index=True)
    author = models.CharField(_('author'), max_length=128)
    author_email = models.EmailField(
        _('author email'), max_length=128, null=True, blank=True,
        help_text=_('Used only to display gravatar and send notifications.'))
    image = models.ImageField(_('image'), upload_to='entry/image/', null=True, blank=True)
    promo = models.BooleanField(_('promoted'), default=False)
    in_stream = models.BooleanField(_('in stream'), default=True)
    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('categories'))
    first_published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    canonical_url = models.URLField(_('canonical link'), null=True, blank=True)
    gallery = models.ForeignKey(PhotoGallery, null=True, blank=True)

    objects = models.Manager()
    published_objects = PublishedEntryManager()

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ['-date']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        published_now = False
        for lc, ln in settings.LANGUAGES:
            if (getattr(self, "published_%s" % lc)
                    and getattr(self, "published_at_%s" % lc) is None):
                now = datetime.now()
                setattr(self, "published_at_%s" % lc, now)
                if self.first_published_at is None:
                    self.first_published_at = now
                    published_now = True
        super(Entry, self).save(*args, **kwargs)
        if published_now and self.pk is not None:
            self.notify_author_published()

    def clean(self):
        for lc, ln in settings.LANGUAGES:
            if (getattr(self, "published_%s" % lc) and
                    not getattr(self, "slug_%s" % lc)):
                raise ValidationError(
                    ugettext("Published entry should have a slug in relevant language (%s).") % lc)

    @models.permalink
    def get_absolute_url(self):
        return 'migdal_entry_%s' % self.type, [self.slug]

    def get_type(self):
        return dict(app_settings.TYPES_DICT)[self.type]

    def notify_author_published(self):
        if not self.author_email:
            return
        site = Site.objects.get_current()
        mail_text = loader.get_template('migdal/mail/published.txt').render(
            Context({
                'entry': self,
                'site': site,
            }))
        send_mail(
            ugettext(u'Your story has been published at %s.') % site.domain,
            mail_text, settings.SERVER_EMAIL, [self.author_email]
        )

    def inline_html(self):
        for att in self.attachment_set.all():
            if att.file.name.endswith(".html"):
                with open(att.file.path) as f:
                    yield f.read()


add_translatable(Entry, languages=app_settings.OPTIONAL_LANGUAGES, fields={
    'needed': models.CharField(_('needed'), max_length=1, db_index=True, choices=(
                ('n', _('Unneeded')), ('w', _('Needed')), ('y', _('Done'))),
                default='n'),
})

TEXTILE_HELP = _('Use <a href="https://txstyle.org/article/44/an-overview-of-the-textile-syntax">Textile</a> syntax.')

add_translatable(Entry, {
    'slug': SlugNullField(unique=True, db_index=True, null=True, blank=True),
    'title': models.CharField(_('title'), max_length=255, null=True, blank=True),
    'lead': TextileField(
        _('lead'), markup_type='textile_pl', null=True, blank=True, help_text=TEXTILE_HELP),
    'body': TextileField(
        _('body'), markup_type='textile_pl', null=True, blank=True, help_text=TEXTILE_HELP),
    'place': models.CharField(_('place'), null=True, blank=True, max_length=256),
    'time': models.CharField(_('time'), null=True, blank=True, max_length=256),
    'published': models.BooleanField(_('published'), default=False),
    'published_at': models.DateTimeField(_('published at'), null=True, blank=True),
})


class Attachment(models.Model):
    file = models.FileField(_('file'), upload_to='entry/attach/')
    entry = models.ForeignKey(Entry)

    def url(self):
        return self.file.url if self.file else ''


def notify_new_comment(sender, instance, created, **kwargs):
    if created and isinstance(instance.content_object, Entry) and instance.content_object.author_email:
        site = Site.objects.get_current()
        mail_text = loader.get_template('migdal/mail/new_comment.txt').render(
            Context({
                'comment': instance,
                'site': site,
            }))
        send_mail(
            ugettext(u'New comment under your story at %s.') % site.domain,
            mail_text, settings.SERVER_EMAIL, 
            [instance.content_object.author_email]
        )
models.signals.post_save.connect(notify_new_comment, sender=XtdComment)


def spamfilter(sender, comment, **kwargs):
    """Very simple spam filter. Just don't let any HTML links go through."""
    if re.search(r"<a\s+href=", comment.comment):
        fields = (
            comment.user, comment.user_name, comment.user_email,
            comment.user_url, comment.submit_date, comment.ip_address,
            comment.followup, comment.comment)
        mail_managers(
            u"Spam filter report",
            (u"""This comment was turned down as SPAM: \n""" +
             """\n%s""" * len(fields) +
             """\n\nYou don't have to do anything.""") % fields)
        return False
    return True
# comment_will_be_posted.connect(spamfilter)
