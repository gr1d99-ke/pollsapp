from django.shortcuts import reverse

from polls.tests.polls_base_test_case import create_question, PollsBaseTestCase


class QuestionDetailViewTestCase(PollsBaseTestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """

        future_question = create_question("Future question.", 30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """

        past_question = create_question("Past question", -3)
        url = reverse("polls:detail", args=(past_question.id, ))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)
