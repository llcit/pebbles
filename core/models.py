from django.db import models



class Language(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name
