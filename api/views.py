from django.http import JsonResponse
from rest_framework.views import APIView
from users.models import Users
from api.serializers import UserSerializer
from rest_framework import generics
from faker import Faker
from rest_framework.response import Response
from rest_framework import status
import itertools as it
from django.core.cache import cache


class UsersApiView(generics.ListCreateAPIView):
    """
    get:
    Return all users with pagination if no params are given. Filter is available too.
    if 'from' and 'to' params are given, filter will be activated. Filter the users by birthday '%d%m'. For example from=0101 to=3112
    example: /api/v1/users?from=0101&to=0202


    post:
    Create new users from given json
    Save items, in which all the fields are given and email is unique to db
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = Users.objects.all()
        date_from = self.request.GET.get('from', False)
        date_to = self.request.GET.get('to', False)
        if date_from and date_to and date_from.isdecimal() and date_to.isdecimal():
            queryset = queryset.filter(
                birthday__month__gte=date_from[2:4],
                birthday__day__gte=date_from[:2],
                birthday__month__lte=date_to[2:4],
                birthday__day__lte=date_to[:2])
        return queryset

    def create(self, request, *args, **kwargs):
        data_list = []
        for val in request.data:
            serializer = self.get_serializer(data=val)
            if serializer.is_valid():
                self.perform_create(serializer)
                data_list.append(serializer.data)
            else:
                data_list.append(serializer.errors)

        return JsonResponse(data_list, safe=False)


class AverageAgeView(APIView):
    """
    Calculates and returns average of user ages.
    Only first request will take a little bit more than next requests as after first request
    age sums and age len which helps to calculate average are cached. age sums and age len will
    be updated only whenever new record added in signals.py and at 00:00 clock every day by celery.
    Because some users' birthday may be next day so that means ages could change every day.
    """
    def get(self, *args, **kwargs):
        # First get all cached items
        objects = cache.get('objects')
        cache_age_sum = cache.get('cache_age_sum')
        cache_age_len = cache.get('cache_age_len')

        # objects is None during only first request.
        if objects is None:
            objects = Users.objects.all()
            cache.set('objects', objects, 86400)

        # cache_age_sum and cache_age_len will be updated whenever new record added in signals.py
        # and by celery
        if cache_age_sum is None or cache_age_len is None:
            age_sum = 0
            for user in objects:
                age_sum += user.get_age()

            cache_age_sum = age_sum
            cache.set('cache_age_sum', cache_age_sum, 86400)
            cache_age_len = len(objects)
            cache.set('cache_age_len', cache_age_len, 86400)

        average = round(cache_age_sum / cache_age_len)

        return JsonResponse({
            "average_age": average,
            "cache_age_len": cache_age_len,
            "cache_age_sum": cache_age_sum,
        })


class LetterDigitView(APIView):
    """
    Must be given '{"arg": "a2B"}' as post data to calculate
    and return the all possible combinations of the arg.
    """
    def post(self, request):
        if 'arg' in request.data:
            result = self.cap_permutations(request.data["arg"])

            return JsonResponse({
                request.data["arg"]: result
            })

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def cap_permutations(str):
        lu_sequence = []
        for c in str:
            if c.isdigit():
                lu_sequence.append([c])
            else:
                lu_sequence.append([c.lower(), c.upper()])
        return [''.join(x) for x in it.product(*lu_sequence)]


# class FakeDataView(APIView):
#
#     def get(self, *args, **kwargs):
#         fake = Faker()
#         for x in range(100):
#             Users.objects.create(
#                 first_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 email=fake.ascii_email(),
#                 birthday=fake.date_of_birth(),
#             )
#
#         return JsonResponse({
#             "status": "Ok"
#         })
