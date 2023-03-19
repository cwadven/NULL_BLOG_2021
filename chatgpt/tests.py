from django.test import TestCase

from chatgpt.models import Lesson


class ChatGPTTestCase(TestCase):
    def setUp(self):
        pass

    def test_request_lesson_to_chatgpt(self):
        # Given:
        result = Lesson.request_lesson_to_chatgpt()

        # Expect: 교훈이 될 수 있는 좋은 말해줘 라는 문자열이 반환되어야 한다.
        self.assertEqual(result, '교훈이 될 수 있는 좋은 말해줘')

    def test_request_lesson_summary_by_body(self):
        # Given:
        test = 'test'
        result = Lesson.request_lesson_summary_by_body(test)

        # Expect: test 를 1줄로 전부 요약해줘 라는 문자열이 반환되어야 한다.
        self.assertEqual(result, f'{test} 를 1줄로 전부 요약해줘')
