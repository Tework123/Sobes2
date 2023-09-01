def bot_talk(speech):
    nv.say(speech)


# бот слушает
def listen():
    # если пройдет 4 секунды после говорения бота,
    # и нет ответа от абонента - возвращаю результат распознования речи

    # если пройдет 60 секунд с начала говорения бота, видимо,
    # в любом случае останавливаю прослушку и выдают результат

    # если пройдет 1,5 секунды после слов абонента, и он больше ничего не сказал - возвращаю результат
    with nv.listen(('entity1, entity2', 'intent1, intent2', 500, 'OR'),
                   entities=['entity3',
                             'entity4'],
                   intents='intent3,intent5',
                   no_input_timeout=4000,
                   recognition_timeout=60000,
                   speech_complete_timeout=1500, ) as result:
        time.sleep('Как будто слушаю')

        return result.utterance()


# звонок(основная логика, здесь по порядку вызываются остальные функции)
def ring():
    #  бот слушает, возращает распознанный текст
    result_hello = listen()

    # находим сущности
    entities_from_hello = get_entities_hello(result_hello)

    # если абонент ничего не сказал, то просим его повторить
    if not entities_from_hello:

        # говорит бот
        bot_talk(hello_null)

        # бот слушает
        text_from_abonent = listen()

        # находим сущности
        entities_from_hello_try2 = get_entities(text_from_abonent)

        # если абонент снова ничего не сказал, то перезваниваем:)
        if not entities_from_hello_try2:
            bot_talk(hangup_null)

    # если какая-то фраза была распознана, то бот снова говорит в зависимости от фразы пользователя
    bot_talk(entities_from_hello)

    result_recommended = listen()

    entities_from_recommended = get_entities_recommended(result_recommended)

    # если абонент ничего не сказал, то просим его повторить(надо в отдельную функцию вынести повтор)
    if not entities_from_recommended:

        # говорит бот
        bot_talk(hello_null)

        # бот слушает
        text_from_abonent = listen()

        # находим сущности
        entities_from_hello_try2 = get_entities(text_from_abonent)

        # если абонент снова ничего не сказал, то перезваниваем:)
        if not entities_from_hello_try2:
            bot_talk(hangup_null)

    if entities_from_recommended == 'hangup_negative':
        # записываем в лог и базу оценку, данную пользователем нашей компании,
        # благодарим его и кладем трубку
        nv.hangup()

    if entities_from_recommended == 'hangup_positive':
        # записываем в лог и базу оценку, данную пользователем нашей компании,
        # благодарим его и кладем трубку
        nv.hangup()


    # пытаемся уточнить оценку, прогоняем recommended
    else:
        bot_talk(entities_from_recommended)
        result_recommended2 = listen()
        # можно через несколько функций реализовать, в зависимости от ответа пользователя возвращать их
        # может быть while, пока не получим оценку или не выведем из себя пользователя

    # в конце сбросим звонок
    nv.hangup()


# на вход получает распознанный текст абонента
# расшифровываем ответ пользователя из hello
def get_entities_hello(text_from_abonent):
    # пытается найти сущности в распознанном тексте
    entities = text_from_abonent.entities()
    if entities:
        try:
            confirm = entities['confirm']
            if confirm:
                # здесь нужно переключится на звонок и дать команду боту на следующую фразу
                return recommend_main
            else:
                return hangup_wrong_time

            wrong_time = entities['wrong_time']
            if wrong_time:
                return hangup_wrong_time
            repeat = entities['repeat']
            if repeat:
                return hello_repeat
        except:

            # если абонент ничего не ответил
            return False


# расшифровываем ответ пользователя из recommended
def get_entities_recommend(text_from_abonent):
    # пытается найти сущности в распознанном тексте
    entities = text_from_abonent.entities()
    if entities:
        try:
            recommendation_score = entities['recommendation_score']
            recommendation = entities['recommendation']

            if 0 <= recommendation_score <= 8:
                return hangup_negative

            if 8 < recommendation_score <= 10:
                return hangup_positive

            if recommendation == 'negative':
                return recommend_score_negative

            if recommendation == 'neutral':
                return recommend_score_neutral

            if recommendation == 'positive':
                return recommend_score_positive

            if recommendation == 'dont_know':
                return recommend_repeat_2


        except:
            # если абонент ничего не ответил
            return False

# также нужно сделать логи и складывать распознанные ответы пользователя в базу данных,
# по unique полю - это будет его телефон
