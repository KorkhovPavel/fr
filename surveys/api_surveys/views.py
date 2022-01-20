from rest_framework import generics, status
from datetime import datetime
from pytz import timezone
from rest_framework.response import Response
from api_surveys.models import Survey, Answers, UserSurvey
from api_surveys.serializers import SurveyCreateSerializers, SurveyUpdateDeleteSerializers, \
    SurveyViewActiveSerializers, UserSurveyCreateSerializers, CompletedUserSurveysSerializers


class SurveyCreateView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = SurveyCreateSerializers


class SurveyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateDeleteSerializers

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        for q in instance.question.all():
            if q.choices:
                for c in q.choices.all():
                    c.delete()
            q.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# user
class SurveyActiveView(generics.ListAPIView):
    now_utc = datetime.now(timezone('Europe/Moscow'))
    queryset = Survey.objects.filter(start_date__lte=now_utc.date(), end_date__gte=now_utc.date()).all()
    serializer_class = SurveyViewActiveSerializers


class AnswerCreateView(generics.ListAPIView):
    serializer_class = UserSurveyCreateSerializers


class DetailUserView(generics.CreateAPIView):
    queryset = Answers.objects.filter().all()
    print(UserSurvey.objects.select_related('user_survey_question'))
    serializer_class = CompletedUserSurveysSerializers
