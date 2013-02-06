from django.contrib import admin
from news.models import Section, Article, ArticleImage, ArticleAttachment
from news.forms import AdminArticleForm
from news.utils import can_tweet
from django.utils.functional import curry


class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    fields = ["image_path"]


class ArticleAttachmentInline(admin.TabularInline):
    model = ArticleAttachment
    fields = ["file_path"]


class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'

    list_display = ['title', 'section', 'published_flag']
    list_filter = ['section']
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

    fields = [
        "section",
        "title",
        "slug",
        "author",
        "summary",
        "content",
        "publish",
    ]

    form = AdminArticleForm
    inlines = [
        ArticleImageInline,
        ArticleAttachmentInline
    ]

    def published_flag(self, obj):
        return bool(obj.published)
    published_flag.short_description = "Published"
    published_flag.boolean = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs.get("request")
        if db_field.name == "author":
            ff = super(ArticleAdmin,
                       self).formfield_for_dbfield(db_field, **kwargs)
            ff.initial = request.user.id
            return ff
        return super(ArticleAdmin,
                     self).formfield_for_dbfield(db_field, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        kwargs.update({
            "formfield_callback": curry(self.formfield_for_dbfield,
                                        request=request),
        })
        return super(ArticleAdmin, self).get_form(request, obj, **kwargs)

    def save_form(self, request, form, change):
        # this is done for explicitness that we want form.save to commit
        # form.save doesn't take a commit kwarg for this reason
        return form.save()

admin.site.register(Section, SectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage)
admin.site.register(ArticleAttachment)
