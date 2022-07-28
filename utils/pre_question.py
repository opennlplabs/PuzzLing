def pre_question(question):
    question = question.strip().split(' ')
    # remove the Alphabet ID
    if question[0].isnumeric():
        question = ' '.join(question[1:])
    else:
        question = ' '.join(question)

    return question

# if question.endswith('\n'):
#    question = question.replace('\n', '')
