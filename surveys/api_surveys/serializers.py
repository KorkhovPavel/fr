from rest_framework import serializers

from api_surveys.models import *


class ChoicesCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('id','choices_answer',)


class QuestionCreateSerializers(serializers.ModelSerializer):
    choices = ChoicesCreateSerializers(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id','question_text', 'question_type', 'choices')


class SurveyCreateSerializers(serializers.ModelSerializer):
    question = QuestionCreateSerializers(many=True)

    class Meta:
        model = Survey
        fields = ('id','title', 'start_date', 'end_data', 'description', 'question')

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


class ChoicesUpdateDeleteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('id','choices_answer',)


class QuestionUpdateDeleteSerializers(serializers.ModelSerializer):
    choices = ChoicesUpdateDeleteSerializers(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id','question_text', 'question_type', 'choices')


class SurveyUpdateDeleteSerializers(serializers.ModelSerializer):
    question = QuestionUpdateDeleteSerializers(many=True, required=False)

    class Meta:
        model = Survey
        fields = ('id','title', 'start_date', 'end_data', 'description', 'question')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_data = validated_data.get('end_data', instance.end_data)
        instance.description = validated_data.get('description', instance.description)
        print(instance.question.all())
        for q in instance.question.all():
            if q.choices:
                for c in q.choices.all():
                    c.delete()
            q.delete()
        print(instance.question.all())

        for question in validated_data['question']:
            question_dict = dict(question)
            if 'choices' in question_dict:
                del question_dict['choices']
            question_id = Question.objects.create(survey_id=instance, **question_dict)
            if 'choices' in dict(question):
                for choices in question['choices']:
                    Choices.objects.create(question_id=question_id, **dict(choices))
            instance.question.add(question_id)














        instance.save()
        return instance


class SurveyViewActiveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class AnswerCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'
