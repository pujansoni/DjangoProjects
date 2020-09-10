from csv import DictReader

from django.core.management import BaseCommand

from corona_world_statistics.models import CoronaStats


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from worldometer_data.csv into our CoronaStats model"

    def handle(self, *args, **options):
        if CoronaStats.objects.exists():
            print('CoronaStats data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Creating data")
        for row in DictReader(open('./worldometer_data.csv')):
            corona = CoronaStats()
            corona.country = row['Country']
            corona.continent = row['Continent']
            corona.population = row['Population'] if row['Population'] else 0
            corona.total_cases = row['TotalCases'] if row['TotalCases'] else 0
            corona.new_cases = row['NewCases'] if row['NewCases'] else 0
            corona.total_deaths = row['TotalDeaths'] if row['TotalDeaths'] else 0
            corona.new_deaths = row['NewDeaths'] if row['NewDeaths'] else 0
            corona.total_recovered = row['TotalRecovered'] if row['TotalRecovered'] else 0
            corona.new_recovered = row['NewRecovered'] if row['NewRecovered'] else 0
            corona.active_cases = row['ActiveCases'] if row['ActiveCases'] else 0
            corona.serious_cases = row['SeriousCases'] if row['SeriousCases'] else 0
            corona.cases_per_million = row['CasesPerMillion'] if row['CasesPerMillion'] else 0
            corona.deaths_per_million = row['DeathsPerMillion'] if row['DeathsPerMillion'] else 0
            corona.total_tests = row['TotalTests'] if row['TotalTests'] else 0
            corona.tests_per_million = row['TestsPerMillion'] if row['TestsPerMillion'] else 0
            corona.who_region = row['WHORegion']
            corona.save()
