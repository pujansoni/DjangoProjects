from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from corona_world_statistics.models import CoronaArticles
from pytz import UTC

import itertools


DATETIME_FORMAT = '%m/%d/%Y'


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from corona_articles.csv into our CoronaArticles model"

    def handle(self, *args, **options):
        if CoronaArticles.objects.exists():
            print('CoronaArticles data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading first 500 records")
        for row in itertools.islice(DictReader(open('./corona_articles.csv', newline='', encoding='utf-8')), 500):
            corona = CoronaArticles()
            # raw_date = row['DateAdded']
            # add_date = UTC.localize(
            #     datetime.strptime(raw_date, DATETIME_FORMAT))
            # corona.date_added = row['DateAdded']
            corona.author = row['Author']
            corona.title = row['Title']
            corona.abstract = row['Abstract']
            corona.year = row['Year'] if row['Year'] else 0
            corona.journal_publisher = row['JournalPublisher']
            corona.volume = row['Volume']
            corona.issue = row['Issue']
            corona.pages = row['Pages']
            corona.accession_number = row['AccessionNumber']
            corona.doi = row['DOI']
            corona.url = row['URL']
            corona.name_of_database = row['Database']
            corona.database_provider = row['DatabaseProvider']
            corona.language = row['Language']
            corona.keywords = row['Keywords']
            corona.save()
