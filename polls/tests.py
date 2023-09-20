from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.test import TestCase
import datetime
from . import models
from django.test import client
from django.urls import reverse
# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    date = timezone.now() + datetime.timedelta(days=days)
    return models.Question.objects.create(question_text=question_text, pub_date=date)


class QuestionIndexViewTests(TestCase):
    # note:
    # django creates a database for each test fuction that's why the function 'test_no_questions' would be effective
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There're no questions available")
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_past_question(self):
        question = create_question('Past Question.', days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions_list'], [question]
        )

    def test_future_question(self):
        create_question("Future Question.", days=20)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'There\'re no questions available')
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_past_and_future_question(self):
        past_question = create_question('Past Question.', days=-20)
        create_question('Future Question.', days=20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions_list'], [past_question])

    def test_two_past_questions(self):
        past_question1 = create_question('Past Question1.', days=-20)
        past_question2 = create_question('Past Question2.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions_list'], [
            past_question1, past_question2])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question('Future Question.', days=13)
        response = self.client.get(
            reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question('Past Question.', days=-13)
        response = self.client.get(
            reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
