def del_instance(instance):
    """
    clear data instance
    """
    for q in instance.question.all():
        if q.choices:
            for c in q.choices.all():
                c.delete()
        q.delete()


def create_data_update(validated_data, instance, db_01, db_02):
    """
    create data in db (for func update)
    """
    for question in validated_data['question']:
        question_dict = dict(question)
        if 'choices' in question_dict:
            del question_dict['choices']
        question_id = db_01.objects.create(survey_id=instance, **question_dict)
        if 'choices' in dict(question):
            for choices in question['choices']:
                db_02.objects.create(question_id=question_id, **dict(choices))
        instance.question.add(question_id)
