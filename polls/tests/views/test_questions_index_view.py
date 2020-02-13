from django.shortcuts import reverse

from polls.tests.polls_base_test_case import create_question, PollsBaseTestCase


class QuestionIndexViewTestCase(PollsBaseTestCase):
    def test_no_questions(self):
        """
        If no questions exists, it should display appropriate message
        """

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """

        create_question("Past question.", -30)
        response = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """

        create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """

        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """

        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-3)
        response = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [
                '<Question: Past question 2.>',
                '<Question: Past question 1.>'
            ]
        )
