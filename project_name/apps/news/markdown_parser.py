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
    md = markdown.Markdown(['extra','codehilite'])

    for iref in re.findall(img_ref_re, text):
        img_id = iref[7]
        alt_txt = iref[0]
        try:
            fp_img= File.objects.get(pk=img_id)
            md.references[img_id] = (fp_img.url, alt_txt)
        except ObjectDoesNotExist:
           pass

    for lref in re.findall(reference_re, text):
        a_id = lref[7]
        alt_txt = lref[0]
        try:
            fa = File.objects.get(pk=a_id)
            md.references[a_id] = (fa.url, alt_txt)
        except ObjectDoesNotExist:
            pass


    return md.convert(text)
