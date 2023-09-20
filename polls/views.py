from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from . import models
from django.views import generic
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return models.Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = models.Question
    template_name = 'polls/detail.html'


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


class ResultView(generic.DetailView):
    model = models.Question
    template_name = 'polls/results.html'
