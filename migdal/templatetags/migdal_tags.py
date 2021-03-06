# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.shortcuts import get_object_or_404
from django_comments_xtd.models import XtdComment
import django_comments as comments
import django
from django import template
from migdal import app_settings
from migdal.models import Category, Entry

register = template.Library()


if django.VERSION < (1, 8):
    # See https://docs.djangoproject.com/en/2.2/releases/1.8/#rendering-templates-loaded-by-get-template-with-a-context
    context_for_get_template = template.Context
else:
    context_for_get_template = lambda x: x



@register.simple_tag(takes_context=True)
def entry_begin(context, entry, detail=False):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_begin.html' % entry.type,
        'migdal/entry/entry_begin.html',
    ))
    context = {
        'request': context['request'],
        'object': entry,
        'detail': detail,
    }
    return t.render(context_for_get_template(context))


@register.simple_tag(takes_context=True)
def entry_short(context, entry):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_short.html' % entry.type,
        'migdal/entry/entry_short.html',
    ))
    context = {
        'request': context['request'],
        'object': entry,
    }
    return t.render(context_for_get_template(context))


@register.simple_tag(takes_context=True)
def entry_promobox(context, entry, counter):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_promobox.html' % entry.type,
        'migdal/entry/entry_promobox.html',
    ))
    context = {
        'request': context['request'],
        'object': entry,
        'counter': counter,
    }
    return t.render(context_for_get_template(context))


@register.inclusion_tag('migdal/categories.html', takes_context=True)
def categories(context, taxonomy):
    context = {
        'request': context['request'],
        'object_list': Category.objects.filter(taxonomy=taxonomy).exclude(entry__isnull=True)
    }
    return context


@register.inclusion_tag('migdal/last_comments.html')
def last_comments(limit=app_settings.LAST_COMMENTS):
    return {
        'object_list': XtdComment.objects.filter(is_public=True, is_removed=False).order_by('-submit_date')[:limit]}


@register.inclusion_tag(['comments/form.html'])
def entry_comment_form(entry):
    return {
            'form': comments.get_form()(entry),
            'next': entry.get_absolute_url(),
        }


@register.simple_tag
def entry_url(slug, lang='pl'):
    entry = get_object_or_404(Entry, **{'slug_%s' % lang: slug})
    return entry.get_absolute_url()
