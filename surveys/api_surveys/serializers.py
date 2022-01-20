from rest_framework import serializers

from api_surveys.models import Choices, Question, Survey, Answers, UserSurveyQuestion, UserSurvey


# create survey
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


# update survey
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
        instance.end_date = validated_data.get('end_data', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        if 'start_date' in validated_data:
            raise serializers.ValidationError({'start_date': 'Error,start_date field cannot be changed'})
        for q in instance.question.all():
            if q.choices:
                for c in q.choices.all():
                    c.delete()
            q.delete()

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


# survey active
class SurveyViewActiveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


# answer survey

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

class CompletedUserSurveysSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'
