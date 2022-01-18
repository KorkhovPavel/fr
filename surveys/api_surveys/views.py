from rest_framework import generics
from datetime import datetime
from pytz import timezone
from rest_framework.response import Response

from api_surveys.models import Question, Choices, Survey
from api_surveys.serializers import SurveyCreateSerializers, QuestionCreateSerializers, ChoicesCreateSerializers, \
    SurveyUpdateDeleteSerializers, ChoicesUpdateDeleteSerializers, QuestionUpdateDeleteSerializers, \
    SurveyViewActiveSerializers, AnswerCreateSerializers


class SurveyCreateView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = SurveyCreateSerializers


class QuestionCreateView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = QuestionCreateSerializers


class ChoicesCreateView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ChoicesCreateSerializers

    def post(self, request, *args, **kwargs):
        d = Question.objects.filter(question_type__in=('Single choice answer',
                                                       'Multiple choice answer')).values_list('id', flat=True).all()
        if int(request.data['question_id']) in list(d):
            return self.create(request, *args, **kwargs)
        return Response(data='Error, type question it should be single choice answer or multiple choice answer')


class SurveyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateDeleteSerializers


class QuestionUpdateDeleteView(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateDeleteSerializers


class ChoicesUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Choices.objects.all()
    serializer_class = ChoicesUpdateDeleteSerializers


# user
class SurveyActiveView(generics.ListAPIView):
    now_utc = datetime.now(timezone('Europe/Moscow'))
    queryset = Survey.objects.filter(start_date__lte=now_utc.date(), end_data__gte=now_utc.date()).all()
    serializer_class = SurveyViewActiveSerializers


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializers
