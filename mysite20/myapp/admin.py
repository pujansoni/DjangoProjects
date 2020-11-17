from django.contrib import admin
from .models import Topic, Course, Student, Order, Review


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price')


class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('student', 'order_status', 'order_date')]
    list_display = ('id', 'student', 'order_status', 'order_date', 'courses_ordered')


# Register your models here.
admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
