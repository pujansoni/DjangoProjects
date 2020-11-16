from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SearchForm, OrderForm, ReviewForm


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})
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
    return render(request, 'myapp/about.html')
    # return HttpResponse("This is an E-learning Website! Search our Topics to find all available Courses.")


def detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    # topic = Topic.objects.get(id=topic_id)
    return render(request, 'myapp/detail.html', {'topic': topic})
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


def findcourses(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            topics = Topic.objects.filter(length=length) if length else Topic.objects.all()
            courselist = []
            for top in topics:
                list1 = list(top.courses.filter(price__lte=max_price))
                courselist = courselist + list1

            return render(request, 'myapp/results.html', {'courselist': courselist, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            # The save_m2m() is used only if we use commit=False option for the save() method. Else the save() will
            # automatically save the many-to-many field data
            form.save_m2m()
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review_stat = form.save()
                course = Course.objects.get(pk=review_stat.course.id)
                course.num_reviews += 1
                course.save()
                return redirect('myapp:index')
            else:
                return render(request, 'myapp/review.html',
                              {'form': form,
                               'rating_message': 'You must enter a rating between 1 and 5!'})
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})
