import json
from django.test import TestCase, RequestFactory
from . import views


class CoreApiTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_users_insert_api(self):
        # Every test needs access to the request factory.

        data = [
            {
                "birthday": "01.03.1989",
                "first_name": "Eike",
                "email": "bartels@baumeister-rosing.de",
                "last_name": "Bartels"
            },
            {
                "first_name": "Hans",
                "last_name": "Peter",
                "email": "azebare102jaha@baumeister-rosing.de",
                "birthday": "30.03.1989"
            },
            {
                "first_name": "Jan",
                "last_name": "Lumbeck",
                "email": "bartels@baumeister-rosing.de",
                "birthday": "02.01.1988"
            }
        ]

        request = self.factory.post('/api/v1/users/', data=json.dumps(data), content_type="application/json")
        response = views.UsersApiView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_average_age_api(self):

        request = self.factory.get('/api/v1/average-age/')
        response = views.AverageAgeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_letter_digit_api(self):
        arg = "a2B"
        request = self.factory.post('/api/v1/letter-digit/', data={"arg": arg})
        response = views.LetterDigitView.as_view()(request)
        calc_result = views.LetterDigitView.cap_permutations(arg)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, json.dumps(calc_result))
