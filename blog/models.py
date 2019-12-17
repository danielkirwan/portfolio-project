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

    """
    def longbody(self):
        return self.body.wrap()
    """

    @keep_lazy_text
    def wrap(self, width=150):
        text = self.body
        """
            A word-wrap function that preserves existing line breaks. Expects that
            existing line breaks are posix newlines.

            Preserve all white space except added line breaks consume the space on
            which they break the line.

            Don't wrap long words, thus the output text may have lines longer than
            ``width``.
            """
        def _generator():
            for line in text.splitlines(True):  # True keeps trailing linebreaks
                max_width = min((line.endswith('\n') and width + 1 or width), width)
                while len(line) > max_width:
                    space = line[:max_width + 1].rfind(' ') + 1
                    if space == 0:
                        space = line.find(' ') + 1
                        if space == 0:
                            yield line
                            line = ''
                            break
                    yield '%s\n' % line[:space - 1]
                    line = line[space:]
                    max_width = min((line.endswith('\n') and width + 1 or width), width)
                if line:
                    yield line

        return ''.join(_generator())

    def pubdate(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title