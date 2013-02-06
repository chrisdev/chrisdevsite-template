
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.db.models import permalink
from django.contrib.auth.models import User
from news.managers import NewsManager
from datetime import datetime
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.contrib.sites.models import Site
from django.conf import settings

from django.utils import simplejson as json


class Section(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse("section_detail", kwargs={"slug": self.slug})


class Article(models.Model):
    """Article model."""
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='published')
    author = models.ForeignKey(User, blank=True, null=True)

    section = models.ForeignKey(Section, related_name="articles",
                                blank=True, null=True)

    summary_html = models.TextField(editable=True)
    content_html = models.TextField(editable=True)

    tweet_text = models.CharField(max_length=140, editable=False)
    # when first revision was created
    created = models.DateTimeField(default=datetime.now,
                                   editable=False)
    # when last revision was create (even if not published)
    updated = models.DateTimeField(null=True, blank=True,
                                   editable=False)
    # when last published
    published = models.DateTimeField(null=True, blank=True,
                                     editable=False)

    view_count = models.IntegerField(default=0, editable=False)

    tags = TaggableManager()

    objects = NewsManager()

    class Meta:
        ordering = ("-published",)
        get_latest_by = "published"
        verbose_name = u'News Article'
        verbose_name_plural = u'News Articles'

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        self.updated_at = datetime.now()
        super(Article, self).save(**kwargs)

    def get_absolute_url(self):
        # if self.published and datetime.now() >= self.published:
        #     name = "article_date_detail"
        #     kwargs = {
        #         "year": self.published.strftime("%Y"),
        #         "month": self.published.strftime("%b"),
        #         "day": self.published.strftime("%d"),
        #         "slug": self.slug,
        #     }

        name = "article_detail_pk"
        kwargs = {"pk": self.pk}


        return reverse(name, kwargs=kwargs)

    def rev(self, rev_id):
        return self.revisions.get(pk=rev_id)

    def current(self):
        "the currently visible (latest published) revision"
        return self.revisions.exclude(published=None).order_by("-published")[0]

    def latest(self):
        "the latest modified (even if not published) revision"
        try:
            return self.revisions.order_by("-updated")[0]
        except IndexError:
            return None


class Revision(models.Model):

    article = models.ForeignKey(Article, related_name="revisions")

    title = models.CharField(max_length=90)
    summary = models.TextField()

    content = models.TextField()

    author = models.ForeignKey(User, related_name="post_revisions")

    updated = models.DateTimeField(default=datetime.now)
    published = models.DateTimeField(null=True, blank=True)

    view_count = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        return 'Revision %s for %s' % (self.updated.strftime('%Y%m%d-%H%M'),
                                       self.article.slug)

    def inc_views(self):
        self.view_count += 1
        self.save()


class ArticleAttachment(models.Model):

    article = models.ForeignKey(Article, related_name="attachments",
                                blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now, editable=False)
    file_path = FilerFileField(null=True, blank=True)



    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"


class ArticleImage(models.Model):

    article = models.ForeignKey(Article,
                                related_name="images",
                                blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now, editable=False)

    image_path = FilerImageField(null=True, blank=True)


    def __unicode__(self):
        if self.pk is not None:
            return "[ %d ]" % self.pk
        else:
            return "deleted image"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
