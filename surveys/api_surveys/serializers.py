from datetime import datetime
from pytz import timezone
from rest_framework import serializers
from api_surveys.additional_functions_serializers import create_data_update, del_instance
from api_surveys.models import Choices, Question, Survey, Answers, UserSurveyQuestion, UserSurvey


# admin

# create choices, question, survey
class ChoicesCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('id', 'choices_answer',)


class QuestionCreateSerializers(serializers.ModelSerializer):
    choices = ChoicesCreateSerializers(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_type', 'choices')


class SurveyCreateSerializers(serializers.ModelSerializer):
    question = QuestionCreateSerializers(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'question')

    def create(self, validated_data):
        date = datetime.now(timezone('Europe/Moscow'))
        if validated_data['start_date'] < date.date() or validated_data['end_date'] < date.date():
            raise serializers.ValidationError('Error date')
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


# update choices, question, survey
class ChoicesUpdateDeleteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('id', 'choices_answer',)


class QuestionUpdateDeleteSerializers(serializers.ModelSerializer):
    choices = ChoicesUpdateDeleteSerializers(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'question_type', 'choices')


class SurveyUpdateDeleteSerializers(serializers.ModelSerializer):
    question = QuestionUpdateDeleteSerializers(many=True, required=False)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'question')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        del_instance(instance)
        create_data_update(validated_data, instance, Question, Choices)
        instance.save()
        return instance


# user

# survey active
class SurveyViewActiveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


# create answer survey
class AnswerCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('answer_text', 'choices_answer_id')


class UserSurveyQuestionCreateSerializers(serializers.ModelSerializer):
    answers = AnswerCreateSerializers(many=True, required=False)

    class Meta:
        model = UserSurveyQuestion
        fields = ('question_id', 'answers')


class UserSurveyCreateSerializers(serializers.ModelSerializer):
    user_survey_question = UserSurveyQuestionCreateSerializers(many=True, required=False)

    class Meta:
        model = UserSurvey
        fields = ('user_id', 'survey_id', 'user_survey_question')

    def create(self, validated_data):
        user_survey_question_data = validated_data.pop('user_survey_question')
        id_user_survey = UserSurvey.objects.create(**validated_data)
        for user_survey_question in user_survey_question_data:
            user_survey_question_dict = dict(user_survey_question)
            if 'answers' in user_survey_question_dict:
                del user_survey_question_dict['answers']
            user_survey_question_id = UserSurveyQuestion.objects.create(user_survey_id=id_user_survey,
                                                                        **user_survey_question_dict)
            if 'answers' in dict(user_survey_question):
                for user_survey in user_survey_question['answers']:
                    Answers.objects.create(user_survey_question_id=user_survey_question_id, **dict(user_survey))
        return id_user_survey


# completed user surveys
class DetailAnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('answer_text', 'choices_answer_id')


# detail user inf
class DetailUserSurveyQuestionSerializers(serializers.ModelSerializer):
    answers = DetailAnswerSerializers(many=True, read_only=True)

    class Meta:
        model = UserSurveyQuestion
        fields = ('question_id', 'answers')
        depth = 1


class DetailUserSurveySerializers(serializers.ModelSerializer):
    user_survey_question = DetailUserSurveyQuestionSerializers(many=True, read_only=True)

    class Meta:
        model = UserSurvey
        fields = ['user_id', 'survey_id', 'user_survey_question']
        depth = 1
