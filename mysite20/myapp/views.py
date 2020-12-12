from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .forms import SearchForm, OrderForm, ReviewForm, RegistrationForm, StudentEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_list'] = Topic.objects.all().order_by('id')[:10]
        return context


# Create your views here.
# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/index.html', {'top_list': top_list})
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
    response = render(request, 'myapp/about.html')
    if not request.COOKIES.get('about_visits'):
        value = 1
        response.set_cookie('about_visits', value)
    else:
        value = int(request.COOKIES.get('about_visits'))
        value = value + 1
        response.set_cookie('about_visits', value, max_age=300)
    return response
    # return HttpResponse("This is an E-learning Website! Search our Topics to find all available Courses.")


class TopicDetailView(TemplateView):
    template_name = 'myapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
        context['topic'] = topic
        return context


# def detail(request, topic_id):
#     topic = get_object_or_404(Topic, id=topic_id)
#     return render(request, 'myapp/detail.html', {'topic': topic})
    # topic = Topic.objects.get(id=topic_id)
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


def user_login(request):
    if request.method == 'POST':
        next1 = request.POST.get("next")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                request.session.set_expiry(3600)
                if next1:
                    return redirect(next1)
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return render(request, 'myapp/error.html', {'message': 'Your account is disabled'})
        else:
            return render(request, 'myapp/error.html', {'message': 'Invalid Login Details'})
    else:
        return render(request, 'myapp/login.html')


@login_required(login_url='/myapp/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required(login_url='/myapp/login/')
def myaccount(request):
    # Here we will use the is_staff method to determine weather this is an admin or a student.
    # As we have two types of users at the moment this method is helpful, else we have to modify the built-in User model
    # and change the permissions for each type of user
    if not request.user.is_staff:
        student = Student.objects.get(username=request.user.username)
        # return HttpResponse(student.get_full_name())
        return render(request, 'myapp/myaccount.html',
                      {'full_name': student.get_full_name(),
                       'topics_interested': student.interested_in.all(),
                       'orders': student.orders.all()})
    else:
        return render(request, 'myapp/error.html', {'message': 'You are not a registered student!'})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Setting the chosen password
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Saving the related models data
            form.save_m2m()
            login(request, user)
            request.session['last_login'] = str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            request.session.set_expiry(3600)
            return HttpResponseRedirect(reverse('myapp:index'))
        else:
            return render(request, 'myapp/register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'myapp/register.html', {'form': form})


@login_required
def edit(request):
    student = Student.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = StudentEditForm(data=request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myapp:index'))
    else:
        form = StudentEditForm(instance=student)
        return render(request, 'myapp/edit.html', {'form': form, 'student': student})


@login_required(login_url='/myapp/login/')
def myorders(request):
    if not request.user.is_staff:
        student = Student.objects.get(username=request.user.username)
        orders = student.orders.all()
        return render(request, 'myapp/myorders.html', {'orders': orders})
    else:
        return render(request, 'myapp/error.html', {'message': 'You are not a registered student!'})
