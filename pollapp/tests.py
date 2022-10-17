import datetime
from time import time
from urllib import response
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.urls import reverse

# this is a django.test.TestCase subclass that creates a Question instance with a pub_date in the future.
# we then check the output of was_pub_recently() which *should* be falsey.

# THIS IS FROM THE DJANGO TUTORIAL WEBSITE, ABOUT TESTING: 
"""
When testing, more is better¶
It might seem that our tests are growing out of control. 
At this rate there will soon be more code in our tests than in our application, and the repetition is unaesthetic, 
compared to the elegant conciseness of the rest of our code.

It doesnt matter. Let them grow. For the most part, you can write a test once and then forget about it. 
It will continue performing its useful function as you continue to develop your program.

Sometimes tests will need to be updated. Suppose that we amend our views 
so that only Questions with Choices are published. In that case, many of our existing tests will fail - 
-telling us exactly which tests need to be amended to bring them up to date, 
so to that extent tests help look after themselves.

At worst, as you continue developing, you might find that you have some tests that are now redundant. 
Even thats not a problem; in testing redundancy is a good thing.

As long as your tests are sensibly arranged, they wont become unmanageable. 
Good rules-of-thumb include having:

- a separate TestClass for each model or view
- a separate test method for each set of conditions you want to test
- test method names that describe their function
- if you can't test a piece of code, there's a good chance it needs to be refactored or removed. 
"""


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        # this method looks at the future_question was_pub_recently(), and is expecting False. This returns True however,
        # so the test fails.
        self.assertIs(future_question.was_pub_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently returns True for questions whose pub_date is within the last day. 
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_pub_recently(), True)

    def test_was_published_recently_with_recent_question(self):
        """
        was_pub_recently returns truthy for questions whose pub_date is within the last day. 
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_pub_recently(), True)


def create_question(question_text, days):
    """
    create a question with the given question_text and published the given number of 
    days offset to now. negative for questions published in the past, 
    positive for questions that have yet to be published. 
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no question exists, an appropriate message is displayed. 
        """
        response = self.client.get(reverse("pollapp:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.content['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text='pollapp:index', days=-30)
        response = self.client.get(reverse("pollapp:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)

    def test_future_question(self):
        """
        questions with a pub date in the future aren't displayed on the index page. 
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("pollapp:index"))
        self.assertContains(response, "No polls are available. ")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        even if past and future questions exist, only past questions are displayed. 
        """
        question = create_question(question_text="Past Question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('pollapp:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)

    def test_two_past_questions(self):
        """
        the questions index page may display multiple quesitons.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("pollapp:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question2, question1],)
        

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future returns a 404 not found. 
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("pollapp:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the detail view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="past question.", days=-5)
        url = reverse("pollapp:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)