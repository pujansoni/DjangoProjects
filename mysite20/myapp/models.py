from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    # The max_length is the required argument for the CharField
    name = models.CharField(max_length=200)
    # This field is required by default?
    length = models.IntegerField(default=12)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    # Here we are defining a Many-to-One relationship from Course to Topic i.e: a topic can have many courses
    # The ForeignKey requires two argument: first the class to which the model is related and the on_delete option
    # The related_name name is used to access the many field in this case it's courses
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, blank=True, default='')
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]

    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True, default='')
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Confirmed'),
        (2, 'On Hold'),
    ]

    courses = models.ManyToManyField(Course)
    # Is the on_delete option appropriate?
    student = models.ForeignKey(Student, related_name='orders', on_delete=models.CASCADE)
    # Do I need to add the max_length attribute?
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        course_str = ''
        for course in self.courses.all():
            course_str += course.title
            course_str += '; '
        return str(self.student) + ': ' + course_str

    def total_cost(self):
        total_price = 0
        for course in self.courses.all():
            total_price += course.price
        return total_price


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return 'Email - ' + self.reviewer + ', Course - ' + self.course.title
