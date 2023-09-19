from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
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


def results(request: HttpRequest, question_id):
    response = "You're looking at the repsonse for the question %s"
    return HttpResponse(response % question_id)


def vote(request: HttpRequest, question_id):
    response = "You're voting on the question %s"
    return HttpResponse(response % question_id)
