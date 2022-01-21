from django.urls import path
from api_surveys.views import *

urlpatterns = [
    # admin
    path('survey/create/', SurveyCreateView.as_view()),
    path('survey/upload-del/<int:pk>/', SurveyUpdateDeleteView.as_view()),
    # user and admin
    path('survey/view/active', SurveyActiveView.as_view()),
    path('answer/create/', AnswerCreateView.as_view()),
    path('answer/detail/', DetailUserView.as_view()),

]
