from rest_framework import serializers

from api_surveys.models import *


class SurveyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class QuestionCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ChoicesCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = '__all__'


class SurveyUpdateDeleteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('title', 'end_data', 'description')


class QuestionUpdateDeleteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ChoicesUpdateDeleteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = '__all__'


class SurveyViewActiveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class AnswerCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'