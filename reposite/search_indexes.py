# search_indexes.py
from haystack import indexes

from .models import ProjectPrototype


class ProjectPrototypeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    creator = indexes.CharField(model_attr='creator')
    origin = indexes.CharField(model_attr='origin', default=None)

    def get_model(self):
        return ProjectPrototype

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
