from django.db import models
import html.entities
import re
import unicodedata
from gzip import GzipFile
from io import BytesIO

from django.utils.functional import SimpleLazyObject, keep_lazy_text, lazy
from django.utils.translation import gettext as _, gettext_lazy, pgettext
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/')

    def summary(self):
        return self.body[:100]

    def pubdate(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title