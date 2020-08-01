from django.db import models


class Pet(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    name = models.CharField(max_length=100)
    submitter = models.CharField(max_length=100)
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=30, blank=True)
    description = models.TextField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    submission_date = models.DateTimeField()
    # Here we used null=True, instead of blank=True in age field cause if blank=True, then the default value stored
    # would be 0 which can suggest that the pet was rescued within a year(1 year), so null=True will put NULL value in
    # the database which indicates that the value is not present
    age = models.IntegerField(null=True)
    # Here there will be a many-to-many relation between pet and vaccine
    # Here blank=True, cause some pets may not have any vaccinations
    vaccinations = models.ManyToManyField('Vaccine', blank=True)


class Vaccine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
