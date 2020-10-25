from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'top_list': top_list})
    # course_list = Course.objects.all().order_by('-title')[:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of topics: ' + '</p>'
    # response.write(heading1)
    # for topic in top_list:
    #     para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
    #     response.write(para)
    # response.write('</br>')
    # heading2 = '<p>' + 'List of courses: ' + '</p>'
    # response.write(heading2)
    # for count, course in enumerate(course_list):
    #     para = '<p>' + str(count + 1) + ': ' + str(course.title) + ' - ' + str(course.price) + '</p>'
    #     response.write(para)
    # return response


def about(request):
    return render(request, 'myapp/about0.html')
    # return HttpResponse("This is an E-learning Website! Search our Topics to find all available Courses.")


def detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    # topic = Topic.objects.get(id=topic_id)
    return render(request, 'myapp/detail0.html', {'topic': topic})
    # response = HttpResponse()
    # heading1 = '<p>' + str(topic.name.upper()) + '</p>'
    # response.write(heading1)
    # heading2 = '<p>' + 'Length: ' + str(topic.length) + ' weeks' + '</p>'
    # response.write(heading2)
    # heading3 = '<p>' + 'Courses:' + '</p>'
    # response.write(heading3)
    # for course in topic.courses.all():
    #     para = '<p>' + '&nbsp;&nbsp;&nbsp;&nbsp;' + str(course.title) + '</p>'
    #     response.write(para)
    # return response
