from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = { 'latest_question_list': latest_question_list }
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    # The above two lines can be replaced with the single as given below.
    # The render() function takes the request object as its first argument, a template name as its second argument
    # and a dictionary as its optional third argument.
    # It returns an HttpResponse object of the given template rendered with the given context.
    # return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # The code above can be replaced by the code below

    # It’s a very common idiom to use get() and raise Http404 if the object doesn’t exist. Django provides a shortcut.
    # Here’s the detail()
    # The get_object_or_404() function takes a Django model as its first argument and an arbitrary number of keyword
    # arguments, which it passes to the get() function of the model’s manager.
    # It raises Http404 if the object doesn’t exist.
    # question = get_object_or_404(Question, pk=question_id)
    # There’s also a get_list_or_404() function, which works just as get_object_or_404() – except using filter()
    # instead of get(). It raises Http404 if the list is empty.
    # return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
