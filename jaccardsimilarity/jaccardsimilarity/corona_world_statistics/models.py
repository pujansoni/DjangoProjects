from django.db import models


class CoronaArticles(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=5000, default='')
    title = models.CharField(max_length=5000, default='')
    abstract = models.CharField(max_length=5000, default='')
    year = models.IntegerField(default=0)
    journal_publisher = models.CharField(max_length=1000, default='')
    volume = models.CharField(max_length=1000, default='')
    issue = models.CharField(max_length=1000, default='')
    pages = models.CharField(max_length=1000, default='')
    accession_number = models.CharField(max_length=1000, default='')
    doi = models.CharField(max_length=1000, default='')
    url = models.CharField(max_length=1000, default='')
    name_of_database = models.CharField(max_length=1000, default='')
    database_provider = models.CharField(max_length=1000, default='')
    language = models.CharField(max_length=1000, default='')
    keywords = models.CharField(max_length=1000, default='')


class CoronaStats(models.Model):
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=100, default='')
    population = models.IntegerField(default=0)
    total_cases = models.IntegerField(default=0)
    new_cases = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)
    new_deaths = models.IntegerField(default=0)
    total_recovered = models.IntegerField(default=0)
    new_recovered = models.IntegerField(default=0)
    active_cases = models.IntegerField(default=0)
    serious_cases = models.IntegerField(default=0)
    cases_per_million = models.IntegerField(default=0)
    deaths_per_million = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    total_tests = models.IntegerField(default=0)
    tests_per_million = models.IntegerField(default=0)
    who_region = models.CharField(max_length=100, default='')

