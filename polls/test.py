import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse


def create_question(question_text, start, end):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=start)
    end_time = timezone.now() + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time, end_date=end_time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_can_vote_during_pub_date(self):
        """can_vote() return True  if vote during polls publish date"""
        time = timezone.now() - datetime.timedelta(days=3)
        present = Question(pub_date=time, end_date=timezone.now() + datetime.timedelta(days=3))
        self.assertIs(present.can_vote(), True)

    def test_can_vote_after_end_date(self):
        """can_vote() return False  if vote after polls end date"""
        time = timezone.now() - datetime.timedelta(days=3)
        after = Question(pub_date=time, end_date=timezone.now() - datetime.timedelta(days=1))
        self.assertIs(after.can_vote(), False)

    def test_can_vote_as_end_date_time(self):
        """can_vote() return False  if vote at same time polls end date"""
        time = timezone.now() - datetime.timedelta(days=3)
        equal = Question(pub_date=time, end_date=time)
        self.assertIs(equal.can_vote(), False)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", start=-5, end=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.",  start=5, end=10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.",start=-30, end=-25)
        create_question(question_text="Future question.", start=30, end=35)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.",  start=-30, end=-25)
        question2 = create_question(question_text="Past question 2.", start=-5, end=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', start=5, end=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',  start=-5, end=10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    def test_count_vote(self):
        """application save the data correctly. """
        question = create_question(question_text='are you 2nd year student?',  start=5, end=10)
        question.choice_set.create(choice_text='yes', votes=1)
        question.choice_set.create(choice_text='no', votes=0)
        response = self.client.get(reverse('polls:results', args=(question.id,)))
        yes_count = response.context.dicts[3]['question'].choice_set.get(pk=1).votes
        no_count = response.context.dicts[3]['question'].choice_set.get(pk=2).votes
        self.assertEqual(yes_count, 1)
        self.assertEqual(no_count, 0)
