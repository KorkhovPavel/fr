from rest_framework import serializers

from api_surveys.models import *


class ChoicesCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('choices_answer',)


class QuestionCreateSerializers(serializers.ModelSerializer):
    choices = ChoicesCreateSerializers(many=True, required=False)

    class Meta:
        model = Question
        fields = ('question_text', 'question_type', 'choices')


class SurveyCreateSerializers(serializers.ModelSerializer):
    question = QuestionCreateSerializers(many=True)

    class Meta:
        model = Survey
        fields = ('title', 'start_date', 'end_data', 'description', 'question')

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        id_survey = Survey.objects.create(**validated_data)
        for question in question_data:
            question_dict = dict(question)
            if 'choices' in question_dict:
                del question_dict['choices']
            question_id = Question.objects.create(survey_id=id_survey, **question_dict)
            if 'choices' in dict(question):
                for choices in question['choices']:
                    Choices.objects.create(question_id=question_id, **dict(choices))
        return id_survey

    def update(self, instance, validated_data):
        question_data = validated_data.pop('question')
        id_survey = Survey.objects.create(**validated_data)
        for question in question_data:
            question_dict = dict(question)
            if 'choices' in question_dict:
                del question_dict['choices']
            question_id = Question.objects.create(survey_id=id_survey, **question_dict)
            if 'choices' in dict(question):
                for choices in question['choices']:
                    Choices.objects.create(question_id=question_id, **dict(choices))
        return id_survey


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
