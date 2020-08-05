from django.db import models


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

