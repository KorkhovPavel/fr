from django.db import models
from django.core.exceptions import ValidationError
from pytz import timezone
from datetime import datetime


# validators
def survey_validator_date(value):
    """
    check date, be greater than current
    :param value:
    :return:
    """
    now_utc = datetime.now(timezone('Europe/Moscow'))
    if value < now_utc.date():
        raise ValidationError('Purchase_Date cannot be in the future.')


def choices_validator_question_type(value):
    """
    checking question type to connect answer options to the question
    :param value:
    :return:
    """
    type_good = Question.objects.filter(question_type__in=('Single choice answer', 'Multiple choice answer')).all()
    type_no_good = Question.objects.filter(question_type='Text answer').all()
    if value not in type_good:
        raise ValidationError('Error, type question it should be single choice answer or multiple choice answer')
    if value in type_no_good:
        raise ValidationError('Error, selection options cannot be connected to the Text answer type ')


# Models
class Survey(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    start_date = models.DateField(verbose_name='start_date', validators=[survey_validator_date])
    end_date = models.DateField(verbose_name='end_date', validators=[survey_validator_date])
    description = models.TextField(verbose_name='description')


class Question(models.Model):
    question_text = models.CharField(max_length=250, verbose_name='question_text')
    survey_id = models.ForeignKey('Survey', on_delete=models.PROTECT, related_name='question', )
    QUESTION_TYPE = [
        ('Text answer', 'Text answer'),
        ('Single choice answer', 'Single choice answer'),
        ('Multiple choice answer', 'Multiple choice answer')
    ]
    question_type = models.CharField(max_length=50, verbose_name='question_type', choices=QUESTION_TYPE)


class Choices(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.PROTECT, related_name='choices',
                                    validators=[choices_validator_question_type])
    choices_answer = models.CharField(max_length=250, verbose_name='choices_answer')


# answer
class UserSurvey(models.Model):
    user_id = models.IntegerField(verbose_name='user_id', null=True, blank=True)
    survey_id = models.ForeignKey('Survey', on_delete=models.PROTECT)


class UserSurveyQuestion(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.PROTECT)
    user_survey_id = models.ForeignKey('UserSurvey', on_delete=models.PROTECT, related_name='user_survey_question')


class Answers(models.Model):
    answer_text = models.CharField(max_length=250, verbose_name='answer', null=True, blank=True, )
    choices_answer_id = models.IntegerField(verbose_name='choices', null=True, blank=True, )
    user_survey_question_id = models.ForeignKey('UserSurveyQuestion', on_delete=models.PROTECT, related_name='answers')
