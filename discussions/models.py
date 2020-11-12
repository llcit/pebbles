from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from model_utils.models import TimeStampedModel


class Post(TimeStampedModel):
    text = models.TextField()
    creator = models.ForeignKey(User)
    subject = models.CharField(max_length=512)
    parent_post = models.ForeignKey('self', blank=True, null=True, related_name='replies')
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.subject))
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.subject


class DiscussionLog(TimeStampedModel):
    user = models.ForeignKey(User)
    discussion = models.ForeignKey(Post)

    def __unicode__(self):
        return str(self.modified)

