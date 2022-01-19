from rest_framework import generics, status
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
    queryset = Survey.objects.filter(start_date__lte=now_utc.date(), end_data__gte=now_utc.date()).all()
    serializer_class = SurveyViewActiveSerializers


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializers

    def post(self, request, *args, **kwargs):
        single_choice_answer = Question.objects.filter(question_type='Single choice answer'). \
            values_list('id', flat=True).values_list('id', flat=True).all()
        multiple_choice_answer = Question.objects.filter(question_type='Multiple choice answer'). \
            values_list('id', flat=True).values_list('id', flat=True).all()
        if int(request.data['question_id']) in list(single_choice_answer):
            valid_answer = Choices.objects.filter(question_id=request.data['question_id']). \
                values_list('choices_answer', flat=True).all()
            if request.data['answer'] in list(valid_answer):
                return self.create(request, *args, **kwargs)
            return Response(data=f'Error, choose one answer from {list(valid_answer)}')
        if int(request.data['question_id']) in list(multiple_choice_answer):
            pass
        return self.create(request, *args, **kwargs)
