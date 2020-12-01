import decimal
from django.contrib import admin
from .models import Topic, Course, Student, Order, Review


def apply_discount(modeladmin, request, queryset):
    for course in queryset:
        course.price = course.price * decimal.Decimal('0.9')
        course.save()


apply_discount.short_description = 'Apply 10%% discount'


class CourseInline(admin.TabularInline):
    model = Course


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price')
    actions = [apply_discount, ]


class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('student', 'order_status', 'order_date')]
    list_display = ('id', 'student', 'order_status', 'order_date', 'courses_ordered')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'length')
    inlines = [CourseInline, ]


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
