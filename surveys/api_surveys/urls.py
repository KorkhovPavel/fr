from django.urls import path
from api_surveys.views import *

urlpatterns = [
    # admin
    path('survey/create/', SurveyCreateView.as_view()),
    path('survey/detail/<int:pk>/', SurveyUpdateDeleteView.as_view()),
    path('question/create/<int:pk>/', QuestionUpdateDeleteView.as_view()),
    path('choices/create/<int:pk>/', ChoicesUpdateDeleteView.as_view()),
    # user
    path('survey/view/active', SurveyActiveView.as_view()),
    path('answer/create/', AnswerCreateView.as_view()),

]
