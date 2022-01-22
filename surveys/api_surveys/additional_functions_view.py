from rest_framework.response import Response


def checking_answers(question_type, answers, choices_list, i):
    """ checking answers with options in the database """
    if question_type == 'Single choice answer':
        if int(answers[0]['choices_answer_id']) not in list(choices_list) and len(answers) != 1:
            return Response(data=f'Error, Answer to the question {i["question_id"]} incorrect')
    elif question_type == 'Multiple choice answer':
        for answer in answers:
            if int(answer['choices_answer_id']) not in list(choices_list):
                return Response(data=f'Error, Answer to the question {i["question_id"]} incorrect')
