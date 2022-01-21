from rest_framework import generics, status
from datetime import datetime
from pytz import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api_surveys.additional_functions_view import checking_answers
from api_surveys.models import Survey, UserSurvey, Choices, Question
from api_surveys.serializers import SurveyCreateSerializers, SurveyUpdateDeleteSerializers, \
    SurveyViewActiveSerializers, UserSurveyCreateSerializers, DetailUserSurveySerializers


# admin
# create choices, question, survey
class SurveyCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SurveyCreateSerializers


# update choices, question, survey
class SurveyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
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
# survey active
class SurveyActiveView(generics.ListAPIView):
    now_utc = datetime.now(timezone('Europe/Moscow'))
    queryset = Survey.objects.filter(start_date__lte=now_utc.date(), end_date__gte=now_utc.date()).all()
    serializer_class = SurveyViewActiveSerializers


# create answer survey
class AnswerCreateView(generics.CreateAPIView):
    serializer_class = UserSurveyCreateSerializers

    def post(self, request, *args, **kwargs):
        for item in request.data['user_survey_question']:
            question_type = Question.objects.filter(id=int(item['question_id'])).values_list('question_type',
                                                                                             flat=True).first()
            choices_list = Choices.objects.filter(question_id=int(item['question_id'])).values_list('id',
                                                                                                    flat=True).all()
            answers = item['answers']
            checking_answers(question_type, answers, choices_list, item)
        return self.create(request, *args, **kwargs)


# detail user inf
class DetailUserView(generics.ListAPIView):
    queryset = UserSurvey.objects.all()
    serializer_class = DetailUserSurveySerializers

    def get(self, request, *args, **kwargs):
        queryset = UserSurvey.objects.select_related('survey_id').filter(user_id=request.data['id']).all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
