from django.db import connection, transaction
from apps.publications.models import Publication


def run():
    cursor = connection.cursor()
    cursor.execute("select * from core_publication")
    for row in cursor.fetchall():

        _, created = Publication.object.get_or_create(dateix=row[2],
            defaults={'data_status':row[1],
                      'date'
                     }
        )
