from django.db import models
from django.core.exceptions import ValidationError
from pytz import timezone
from datetime import datetime


# validators
def validator_date(value):
    """
    check date, be greater than current
    :param value:
    :return:
    """
    now_utc = datetime.now(timezone('Europe/Moscow'))
    if value < now_utc.date():
        raise ValidationError('Purchase_Date cannot be in the future.')


# def validator_question_type(value):
#     """
#     question type check, type must not be Text answer
#     :param value:
#     :return:
#     """
#     d = Question.objects.filter(question_type__in=('Single choice answer',
#                                                    'Multiple choice answer')).all()
#     if value not in d:
#         raise ValidationError('Error, type question it should be single choice answer or multiple choice answer')


# Models
class Survey(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    start_date = models.DateField(verbose_name='start_date', validators=[validator_date])
    end_data = models.DateField(verbose_name='end_data', validators=[validator_date])
    description = models.TextField(verbose_name='description')


class Question(models.Model):
    question_text = models.CharField(max_length=250, verbose_name='question_text')
    survey_id = models.ForeignKey('Survey', on_delete=models.PROTECT)
    QUESTION_TYPE = [
        ('Text answer', 'Text answer'),
        ('Single choice answer', 'Single choice answer'),
        ('Multiple choice answer', 'Multiple choice answer')
    ]
    question_type = models.CharField(max_length=50, verbose_name='question_type', choices=QUESTION_TYPE)


class Choices(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.PROTECT)
    choices_answer = models.CharField(max_length=250, verbose_name='choices_answer')


class Answers(models.Model):
    user_id = models.IntegerField(verbose_name='user_id', null=True, blank=True, )
    answer = models.CharField(max_length=250, verbose_name='answer')
    question_id = models.ForeignKey('Question', on_delete=models.PROTECT)
    survey_id = models.ForeignKey('Survey', on_delete=models.PROTECT)
