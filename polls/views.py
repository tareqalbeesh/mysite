from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from . import models
# Create your views here.


def index(request: HttpRequest):
    latest_questions_list = models.Question.objects.order_by("-pub_date")[:5]
    return render(request, 'polls/index.html', {'latest_questions_list': latest_questions_list})


def detail(request: HttpRequest, question_id):
    # try:
    #     question = models.Question.objects.get(pk=question_id)
    # except models.Question.DoesNotExist:
    #     raise Http404("The question was not found!")
    question = get_object_or_404(models.Question, pk=question_id)

    return render(request, 'polls/detail.html', {"question": question})


def vote(request: HttpRequest, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, models.Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {"error_message": "you didn't select a choice!", 'question': question})
    else:
        # selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # after successful post request it's better to make an redirect response to avoid resubmitting the form when the user presses the back button
        return HttpResponseRedirect(reverse("polls:results", args=[question.id]))


def results(request: HttpRequest, question_id):
    question = models.Question.objects.get(pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
