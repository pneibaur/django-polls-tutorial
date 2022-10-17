from django.http import HttpResponseRedirect # httpresponse isn't needed after you rework the code to use the django shortcut
# from django.template import loader -------- same with this one! 
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
# the generic views from django is a powerful tool! when we use it in the classes below, it can provide some auto generated variables. see below! 
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# here, the ListView generic wants to use a default template name as: <app name>/<model_name>_list.html. so we are reassigning it as 'pollapp/index.html'
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # here we are reassigning the context object name. normally django reads our model (Question), and would provide this for us as: question_list. 
    # since we want to use a different name, we are reassignig it to: 'latest_question_list'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # returns the last 5 published questions, but not including those to be 
        # published in the future.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# by default the detail generic uses a template called <app name>/<model name>_list.html. so we are using template_name to = 'pollapp/index.html' instead. 
class DetailView(generic.DetailView):
    # normally we need to declare a question variable, however, the generic view is providing that for us based on the DB model name: Question. 
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        excludes any questions that haven't been published yet. 
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     # template = loader.get_template('polls/index.html')
#     # return HttpResponse(template.render(context, request))
#     # the lines above are so commonly written, there's a shortcut that django offers! see below.
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     # try: 
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist") ----- this code has a shortcut too! see below: 
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.", 
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always return httpResponseRedirect after successfully handling POST data. 
        # This prevents data from being posted twice if user hits back btn. 
        return HttpResponseRedirect(reverse('pollapp:results', args=(question_id,)))