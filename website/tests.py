from django.test import TestCase, Client
from .views import generate_response, DF


class GenerateResponseTestCase(TestCase):
    def test_generate_response(self):
        # Test case 1: Check if the response is not empty
        query = "What is the score of the game?"
        response = generate_response(query, DF)
        self.assertNotEqual(response, "")

        # Test case 2: Check if the response is a string
        self.assertIsInstance(response, str)

        # Test case 3: Check if a specific query produces the correct response
        query = "Who won the egg bowl last year?"
        expected_response = "Mississippi State won the Egg Bowl last year."
        response = generate_response(query, DF)
        self.assertEqual(response, expected_response)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_process_question_view(self):
        # Test case for process_question view
        response = self.client.post(
            "/process_question/",
            {"question": "Who won the egg bowl last year?"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected behavior

    def test_index_view(self):
        # Test case for index view
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected behavior
