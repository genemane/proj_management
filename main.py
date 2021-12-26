import datetime
import re
from datetime import date, timedelta
import PySimpleGUI as sg
import sqlite3 as sl

sg.theme('Material1')

con =  sl.connect("main_data.db")  #Подключение к базе данных для авторизации и регистрации пользователей
cursor = con.cursor()
fonts = [
    ('Segoe UI', 14),
    ('Segoe UI', 11)
]

def make_main_menu():
    layout = [  # Начальный пресет
        [sg.Text('Добро пожаловать!', font=fonts[0])],
        [sg.Text('Вас приветствует органайзер', font=fonts[0])],
        [sg.Text('*Неверный логин или пароль!', font=fonts[1], key='error_mes', visible=False)],
        [sg.Text('Введите логин  ', font=fonts[1]),
         sg.InputText(size=(20, 1), key='input_main_login')],
        [sg.Text('Введите пароль', font=fonts[1]),
         sg.InputText(size=(20, 1), key='input_main_pass', password_char='*')],
        [sg.Button(button_text=('Войти'), size=(20, 1), key=('enter'))],
        [sg.Text('У Вас нет аккаунта?', font=fonts[1])],
        [sg.Button(button_text=('Зарегистрироваться'), size=(30, 1), key=('register'))],
        [sg.Text('*Ваш аккаунт создан, осталось войти в него!', font=fonts[1], key='complete_ok', visible=False)],
    ]
    return sg.Window('Органайзер', layout, icon=r'1.ico', size=(500, 250), resizable=True, finalize=True, grab_anywhere=True, element_justification='c')
days=[
    '',
    '',
    '',
    '',
    '',
    '',
    '',
]
zadachi=[
    'Прочитать главу 1',
    'Прочитать главу 2',
    'Прочитать главу 3',
    'Выучить определения главы 2',
    'Составить вопросы по главе 3',
    'Выучить определения из глав 2, 3',
    'Составить вопросы по главе 3',
    'Составить конспект по главе 1',
    'Составить карточки терминов 2',
    'Составить план главы 3',
    'Пересказ главы 1',
    'Пересказ главы 2',
    'Пересказ главы 3'
]
que = [  # Массив строк для опроса
    '1. Мне требуется много времени, чтобы “раскачаться” и начать действовать',
    '2. Я планирую мои дела ежедневно',
    '3. Меня выводят из себя и выбивают из привычного графика непредвиденные дела',
    '4. Обычно я намечаю программу на день и стараюсь ее выполнить',
    '5. Мне бывает трудно завершить начатое',
    '6. Я не могу отказаться от начатого дела, даже если оно мне «не по зубам»',
    '7. Я знаю, чего хочу, и делаю все, чтобы этого добиться',
    '8. Я заранее выстраиваю план предстоящего дня',
    '9. Мне более важно то, что я делаю и переживаю в данный момент, а не то, что будет или был',
    '10. Я могу начать делать несколько дел и ни одно из них не закончить',
    '11. Я планирую мои повседневные дела согласно определенным принципам',
    '12. Я считаю себя человеком, живущим «здесь и сейчас»',
    '13. Я не могу перейти к другому делу, если не завершил предыдущего',
    '14. Я считаю себя целенаправленным человеком',
    '15. Вместо того чтобы заниматься делами, я часто попусту трачу время',
    '16. Мне нравится вести дневник и фиксировать в нем происходящее со мной',
    '17. Иногда я даже не могу заснуть, вспомнив о недоделанных делах',
    '18. Мне есть к чему стремиться',
    '19. Мне нравится пользоваться ежедневником и иными средствами планирования времени',
    '20. Моя жизнь направлена на достижение определенных результатов',
    '21. У меня бывают трудности с упорядочением моих дел',
    '22. Мне нравится писать отчеты по итогам работы',
    '23. Я ни к чему не стремлюсь',
    '24. Если я не закончил какое-то дело, то это не выходит у меня из головы',
    '25. У меня есть главная цель в жизни'
]
raspr=[
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    ''
]
# Для будущей версии, если найдем способ вывода многострочного текста в sg.Text
text_opros = 'Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации\n' \
             'Вам предлагается 25 утверждений, касающихся различных сторон Вашей жизни и способов обращения со временем. ' \
             'Введите в поле ту цифру, которая в наибольшей мере характеризует Вас и отражает Вашу точку зрения ' \
             '(1 — полное несогласие, 7 — полное согласие с данным утверждением, 4 — середина шкалы, остальные цифры — промежуточные значения'
count = 0
def make_after_login():
    layout = [  # Пресет после клика кнопки Войти
        [sg.Text(text=que[count], key=('opros'), font=fonts[1]), sg.Slider(range=(1,7), relief = 'groove', orientation='horizontal', tick_interval=1, default_value=4, key='input1')],
        [sg.Button(button_text=('Назад'), size=(10, 1), key=('back')), sg.Button(button_text=('Далее'), size=(10, 1), key=('next'))],
        [sg.Text('Баллы:'), sg.Text('', size=(3, 1), key=('sum'), font=fonts[1])],
        [sg.Button(button_text=('Завершить'), size=(10, 1), key=('end'), visible=False)]
    ]
    return sg.Window('Опрос', layout, size=(1200, 175), resizable=True, finalize=True, grab_anywhere=True, element_justification='c')

open = False
def make_after_login_text():
    layout = [  # Пресет после клика кнопки Войти
        [sg.Text(text='Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации', font=fonts[0])],
        [sg.Text(
            text='Вам предлагается 25 утверждений, касающихся различных сторон Вашей жизни и способов обращения со временем. Введите в поле ту цифру, которая ', font=fonts[1])],
        [sg.Text(
            text='в наибольшей мере характеризует Вас и отражает Вашу точку зрения (1 — полное несогласие, 7 — полное согласие с данным утверждением, 4 — середина ', font=fonts[1])],
        [sg.Text(text='шкалы, остальные цифры — промежуточные значения)', font=fonts[1])],
        [sg.Button(button_text=('Продолжить'), size=(20, 1), key=('end_text'), visible=True)]
]
    return sg.Window('Опрос', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='c')

def make_register():
    layout = [
        [sg.Text('Регистрация', font=fonts[0])],
        [sg.Text('Введите фамилию', font=fonts[1], key=('surname')), sg.Input('', size=(40, 1), key=('input_sur'))],
        [sg.Text('Введите имя', font=fonts[1], key=('name')), sg.Input('', size=(40, 1), key=('input_name'))],
        [sg.Text('Введите отчество', font=fonts[1], key=('patronymic')), sg.Input('', size=(40, 1), key=('input_patr'))],
        [sg.Text('Придумайте логин', font=fonts[1], key=('login')), sg.Input('', size=(40, 1), key=('input_login'))],
        [sg.Text('Придумайте пароль', font=fonts[1], key=('pass')), sg.Input('', size=(28, 1), key=('input_pass'), password_char='*'), sg.Button(button_text='      👁️', font=fonts[1], key=('open_pass'))],
        [sg.Text('Повторите пароль', font=fonts[1], key=('pass_check')), sg.Input('', size=(40, 1), key=('input_check'), password_char='*')],
        [sg.Text('*Пароль должен содержать минимум 8 символов', font=fonts[1])],
        [sg.Button(button_text=('Зарегистрироваться'), size=(20, 1), key=('reg_complete'))],
        [sg.Text('Заполните все поля для завершения регистрации!', font=fonts[1], key='reg_check', visible=False)]
    ]
    return sg.Window('Регистрация', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='c')
def organizer():
    layout = [
        [sg.pin(sg.Button(button_text=(days[0]), size=(10, 1), key=('day1'))),
         sg.pin(sg.Button(button_text=(days[1]), size=(10, 1), key=('day2'))),
         sg.pin(sg.Button(button_text=(days[2]), size=(10, 1), key=('day3'))),
         sg.pin(sg.Button(button_text=(days[3]), size=(10, 1), key=('day4'))),
         sg.pin(sg.Button(button_text=(days[4]), size=(10, 1), key=('day5'))),
         sg.pin(sg.Button(button_text=(days[5]), size=(10, 1), key=('day6'))),
         sg.pin(sg.Button(button_text=(days[6]), size=(10, 1), key=('day7')))]
    ]

    return sg.Window('Органайзер', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='l')
def make_rezult():
    layout = [
        [sg.Text(text='Результаты опроса', font=fonts[0])],
        [sg.Text(text='Количество набранных баллов: '), sg.Text('', size=(3, 1), key=('rez'), font=fonts[1])],
        [sg.Multiline(size=(50,10), key=('rezt'), font=fonts[1], disabled=True)],
        [sg.Button(button_text=('Завершить опрос'), size=(20, 1), key=('opros_complete'))]
    ]
    return sg.Window('Результаты', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='c')
def lk():
    layout = [
        [sg.pin(sg.Text(text="Добро пожаловать, ", font=fonts[0])), sg.pin(sg.Text(text="", key=('namesurname'), font=fonts[0])) ],
        [sg.pin(sg.Button(button_text=('Пройти входной опрос'), size=(20, 1), key=('vhopros'))),
         #в дальнейшем надо рассчитать где-то прогресс в процентах, типа сколько заданий выполнено от общего количества
         sg.pin(sg.Text(text='Ваш прогресс по количеству выполненных заданий составляет ')),
         sg.pin(sg.Text(text='', ))], #вот этот текст менять на проценты
        [sg.Button(button_text=('Перейти в органайзер'), size=(20, 1), key=('org'))],
        [sg.Button(button_text=('Пройти итоговый тест'), size=(20, 1), key=('test'))],
        [sg.Button(button_text=('Выйти из аккаунта'), size=(20, 1), key=('exit'))]
    ]
    return sg.Window('Личный кабинет', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='l')
def date_zadachi():
    layout = [
        [sg.Text(text="Для начала работы распределите задачи по дням:", font=fonts[0])],
        [sg.Text(text=zadachi[0], font=fonts[0]), sg.Combo(days, size=(10,1), key=('com0'), readonly=True)],
        [sg.Text(text=zadachi[1], font=fonts[0]), sg.Combo(days, size=(10,1), key=('com1'), readonly=True)],
        [sg.Text(text=zadachi[2], font=fonts[0]), sg.Combo(days, size=(10,1), key=('com2'), readonly=True)],
        [sg.Text(text=zadachi[3], font=fonts[0]), sg.Combo(days, size=(10,1), key=('com3'), readonly=True)],
        [sg.Text(text=zadachi[4], font=fonts[0]), sg.Combo(days, size=(10,1), key=('com4'), readonly=True)],
        [sg.Text(text=zadachi[5], font=fonts[0], visible=False, key=('zad5')), sg.Combo(days, size=(10,1), key=('com5'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[6], font=fonts[0], visible=False, key=('zad6')), sg.Combo(days, size=(10,1), key=('com6'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[7], font=fonts[0], visible=False, key=('zad7')), sg.Combo(days, size=(10,1), key=('com7'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[8], font=fonts[0], visible=False, key=('zad8')), sg.Combo(days, size=(10,1), key=('com8'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[9], font=fonts[0], visible=False, key=('zad9')), sg.Combo(days, size=(10,1), key=('com9'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[10], font=fonts[0], visible=False, key=('zad10')), sg.Combo(days, size=(10,1), key=('com10'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[11], font=fonts[0], visible=False, key=('zad11')), sg.Combo(days, size=(10,1), key=('com11'), readonly=True, visible=False)],
        [sg.Text(text=zadachi[12], font=fonts[0], visible=False, key=('zad12')), sg.Combo(days, size=(10,1), key=('com12'), readonly=True, visible=False)],
        [sg.Button(button_text=('Начать работу'), size=(20,1), key=('startwork'))]
    ]
    return sg.Window('Распределение задач', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='l')
window = make_main_menu()
score_mas = [0 for x in range(25)]  #Массив ответов в опросе
score_sum = 0
pointer_score = 1                   #Указатель на текущую позицую в массиве
user_logged = ''

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif 'vhopros' in event:
        window.close()
        window=make_after_login_text()
    elif 'exit' in event:
        window.close()
        window=make_main_menu()
    elif 'enter' in event:
        cursor.execute('SELECT pass FROM USER_LOGIN_DATA where login = "' + values['input_main_login'] + '"')
        user_logged = ''.join(str(values['input_main_login']))
        executed_str = ''.join(str(cursor.fetchone()))
        executed_str = re.sub("[^A-Za-z0-9]", "", executed_str)
        cursor.execute('SELECT SURVEY_COMPLETE FROM USER_LOGIN_DATA where login = "' + values['input_main_login'] + '"')
        survey_check = ''.join(str(cursor.fetchone()))
        if executed_str == values['input_main_pass']:
            window.close()
            #if not(survey_check):
            #    window = make_after_login_text()
            #else:
            #    print('Опрос уже пройден')
            #cursor.execute('SELECT pass FROM USER_LOGIN_DATA where name="')
            window=lk()
            window.Element('namesurname').Update(value=cursor.execute('SELECT name FROM USER_LOGIN_DATA'))
            #window.Element('namesurname').Update(value=cursor.execute('SELECT name FROM USER_LOGIN_DATA where pass="'+values['input_main_pass']))

            #window = make_after_login_text()
        else:
            window.Element('error_mes').Update(visible=True)
    elif 'register' in event:
        window.close()
        window = make_register()
    elif 'startwork' in event:
       #Эти данные нужно как-то сохранять в БД
       # i=0
       # while i<13
        raspr[0]=(values['com0'])
        raspr[1]=(values['com1'])
        raspr[2]=(values['com2'])
        raspr[3]=(values['com3'])
        raspr[4]=(values['com4'])
        raspr[5]=(values['com5'])
        raspr[6]=(values['com6'])
        raspr[7]=(values['com7'])
        raspr[8]=(values['com8'])
        raspr[9]=(values['com9'])
        raspr[10]=(values['com10'])
        raspr[11]=(values['com11'])
        raspr[12]=(values['com12'])
        window.close()
        window=organizer()
    elif 'next' in event:
        score_mas[pointer_score] = abs(int(values['input1']) - 8)
        pointer_score += 1
        score_sum = sum(score_mas)
        print(pointer_score)
                                            # Должно быть значение 25 (для тестов используем, например, 3)
        if pointer_score < 25:
            window.Element('opros').Update(value=que[pointer_score-1])
            window.Element('input1').Update(value=4)
            window.Element('sum').Update(value=score_sum)
        if pointer_score == 25:
            window.Element('opros').Update(value=que[pointer_score-1])
            window.Element('next').Update(visible=False)
            window.Element('end').Update(visible=True)
            window.Element('sum').Update(value=score_sum)
    elif 'back' in event:
        window.Element('next').Update(visible=True)
        window.Element('end').Update(visible=False)
        if pointer_score > 0:
            score_sum = sum(score_mas) - score_mas[pointer_score-1]
            window.Element('input1').Update(value=abs(score_mas[pointer_score-1]-8))
            score_mas[pointer_score-1] = 0
            window.Element('sum').Update(value=score_sum)
        if pointer_score > 1:
            pointer_score -= 1
            window.Element('opros').Update(value=que[pointer_score-1])
            window.Element('input1').Update(value='')
    elif 'end_text' in event:
        window.close()
        window = make_after_login()
    elif 'org' in event: #берем today либо из базы данных, либо из функции
        today=date.today()
        izm =timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        days[0]=today
        days[1]=today+izm
        days[2]=today+izm*2
        days[3]=today+izm*3
        days[4]=today+izm*4
        days[5]=today+izm*5
        days[6]=today+izm*6
        window.close()         #Если уже есть дата в БД, то открывается сразу органайзер
        window=date_zadachi()
            # Должно быть значение 24 (для тестов используем, например, 2)
    elif 'end' in event:
        score_sum += int(values['input1'])
        window.close()
        window = make_rezult()
        window.Element('rez').Update(value=score_sum)
        if 0 < score_sum < 59:
            window.Element('rezt').Update(value='Ваш уровень самоорганизации низкий. Вы предпочитаете жить спонтанно, не привязывать свою деятельность к жесткой структуре и целям. Ваше будущее для Вас самого достаточно туманно, Вам не свойственно четко планировать свою ежедневную активность и прилагать волевые усилия для завершения начатых дел, однако это позволяет Вам достаточно быстро и гибко переключаться на новые виды активности, не «застревая» на структурировании своей деятельности.')
        if 58 < score_sum < 117:
            window.Element('rezt').Update(value='Ваш уровень самоорганизации средний. Вы способны сочетать структурированный подход к организации времени своей жизни со спонтанностью и гибкостью, умеете ценить все составляющие Вашего психологического времени и извлекать для себя ценный опыт из многоплановости своей жизни.')
        if 116 < score_sum < 176:
            window.Element('rezt').Update(value='Ваш уровень самоорганизации высокий. Вам свойственно видеть и ставить цели, планировать свою деятельность, в том числе с помощью внешних средств, и, проявляя волевые качества и настойчивость, идти к ее достижению. Возможно, в отдельных видах деятельности Вы можете быть чрезмерно структури- рованны, организованны и недостаточно гибки. Тем не менее Вы достаточно эффективно можете структурировать свою деятельность.')
        sql = 'UPDATE USER_LOGIN_DATA SET ORG_DATE = ?, SURVEY_COMPLETE = ? WHERE login = "' + user_logged + '"'
        data = [
           # (datetime.now(), 1)
        ]
        with con:
            con.executemany(sql, data)
    elif 'open_pass' in event:
        if open:
            open = False
            window.Element('input_pass').Update(password_char='*')
        else:
            open = True
            window.Element('input_pass').Update(password_char='')
    elif 'reg_complete' in event:
        if str(values['input_pass']).__len__() < 8:
            window.Element('reg_check').Update(value='Пароль содержит меньше 8-ми символов!', visible=True)
        elif values['input_pass'] != values['input_check']:
            window.Element('reg_check').Update(value='Пароли не совпадают!', visible=True)
        elif values['input_sur'] == '' or values['input_name'] == '' or values['input_patr'] == '' or values['input_login'] == '' or values['input_pass'] == '' or values['input_check'] == '':
            window.Element('reg_check').Update(value='Заполните все поля для завершения регистрации!',visible=True)
        else:
            sql = 'INSERT INTO USER_LOGIN_DATA (id, surname, name, patronymic, login, pass, admin) values(?, ?, ?, ?, ?, ?, ?)'
            last = ''.join(str(cursor.execute("SELECT Id FROM USER_LOGIN_DATA ORDER BY Id DESC LIMIT 1").fetchone()))
            last = int(''.join(i for i in last if i.isdigit()))+1
            data = [
                (last, values['input_sur'], values['input_name'], values['input_patr'], values['input_login'], values['input_pass'], 0)
            ]
            with con:
                con.executemany(sql, data)
            window.close()
            window = make_main_menu()
            window.Element('complete_ok').Update(visible=True)

    elif 'opros_complete':
        window.close()
        window = lk()
window.close()
