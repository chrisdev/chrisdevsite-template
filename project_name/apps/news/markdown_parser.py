import markdown
import re
from markdown.inlinepatterns import IMAGE_REFERENCE_RE, REFERENCE_RE
from news.models import ArticleImage
from filer.models import File
from django.core.exceptions import ObjectDoesNotExist
img_ref_re = re.compile(IMAGE_REFERENCE_RE)
reference_re = re.compile(REFERENCE_RE)
pdf_doc_pattern = r'^.*\.(doc|DOC|pdf|PDF)'


def parse(text):
    """
    This is a test of md references
    Ok now the ids
    ![Alt text 2][1]
    """
    md = markdown.Markdown(['codehilite', 'flex_video', 'tables'])
    for iref in re.findall(img_ref_re, text):
        img_id = iref[7]
        try:
            image = ArticleImage.objects.get(pk=int(img_id))
            md.references[img_id] = (image.image_path.url, '')
        except ObjectDoesNotExist:
            pass

    for lref in re.findall(reference_re, text):
        doc_name = lref[7]
        try:
            doc = File.objects.get(name=doc_name.lower())
            md.references[doc_name] = (doc.url, doc.name)
        except ObjectDoesNotExist:
            pass


    return md.convert(text)
