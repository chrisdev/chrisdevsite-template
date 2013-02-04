from .models import Monthly, Publication
from dateutil import parser
from dateutil.rrule import MONTHLY
from dateutil.rrule import rrule

def last_valid_pubdate():
    """
    gets the last embargo  date
    """
    try:
        return Publication.objects.all().order_by(
            '-publication_date__id')[0].publication_date
    except IndexError:
        return None


def generate_monthly(start, end):
    """
    A utility method to generate
    """
    dstart = parser.parse(start)
    dend = parser.parse(end)
    rr = rrule(MONTHLY, dtstart=dstart,
               until=dend, bymonthday=(-1))
    for dd in rr:
        _, cretated = Monthly.objects.get_or_create(dateix=dd,
            defaults={'dateix': dd}
            )

