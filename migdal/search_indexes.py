import datetime
from django.conf import settings
from haystack import indexes
from fnpdjango.utils.models.translation import add_translatable_index, localize_field
from migdal.models import Entry


class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(null=True,
        model_attr=localize_field('body', settings.LANGUAGE_CODE),
        document=True)
    date = indexes.DateTimeField(indexed=True, model_attr="date")
    author = indexes.CharField(model_attr="author")

    def get_model(self):
        return Entry


add_translatable_index(EntryIndex, {
    'title': indexes.CharField(null=True),
    'lead': indexes.CharField(null=True),
    })

add_translatable_index(EntryIndex, {
    'title': indexes.CharField(null=True),
    'lead': indexes.CharField(null=True),
    'body': indexes.CharField(null=True)
    }, 
    (lang for lang in settings.LANGUAGES if lang[0] != settings.LANGUAGE_CODE)
)
