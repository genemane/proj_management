import PySimpleGUI as sg
import sqlite3 as sl

con =  sl.connect("main_data.db")  #Подключение к базе данных для авторизации и регистрации пользователей
cursor = con.cursor()

def make_main_menu():
    layout = [  # Начальный пресет           [sg.Text('Enter the value',justification='center',size=(100,1))],
        [sg.Canvas(size=(0, 10))],
        [sg.Text('Добро пожаловать!', justification='center',size=(35,0))],
        [sg.Text('Вас приветствует органайзер', justification='center',size=(35,0))],
        [sg.Text('Неверный логин или пароль!', key='error_mes', visible=False)],
        [sg.Canvas(size=(0, 5))],
        [sg.Text('Введите логин  '), sg.InputText(size=(20, 1), key='input_main_login')],
        [sg.Canvas(size=(0, 2))],
        [sg.Text('Введите пароль'), sg.InputText(size=(20, 1), key='input_main_pass', password_char='*')],
        [sg.Canvas(size=(0, 15))],
        [sg.Canvas(size=(86, 0), key=('cen_left_canvas1')), sg.Button(button_text=('Войти'), size=(10, 1), key=('enter'))],
        [sg.Canvas(size=(0, 5))],
        [sg.Text('У Вас нет аккаунта?', justification='center', size=(35,0))],
        [sg.Canvas(size=(58, 0), key=('cen_left_canvas2')), sg.Button(button_text=('Зарегистрироваться'), size=(17, 1), key=('register'))], #[sg.Button('Enter','center',size=(100,1))]
        [sg.Text('Ваш аккаунт создан, осталось войти в него!',justification='center',size=(35,0), key='complete_ok', visible=False)],
        [sg.Canvas(size=(0, 25))]

        #[sg.Canvas(size=(150, 10))],
        #[sg.Canvas(size=(80, 0)), sg.Text(text='Добро пожаловать!')],
        #[sg.Canvas(size=(55, 0)), sg.Text(text='Вас приветствует органайзер')],
        #[sg.Canvas(size=(0, 0)), sg.Text(text='Неверный логин или пароль!', key='error_mes', visible=False)],
        #[sg.Canvas(size=(0, 0)), sg.Text(text='Введите логин  '), sg.InputText(size=(20, 1), key='input_main_login')],
        #[sg.Canvas(size=(150, 5))],
        #[sg.Canvas(size=(0, 0)), sg.Text(text='Введите пароль'), sg.InputText(size=(20, 1), key='input_main_pass', password_char='*')],
        #[sg.Canvas(size=(150, 15))],
        #[sg.Canvas(size=(90, 1), key=('cen_left_canvas1')), sg.Button(button_text=('Войти'), size=(10, 1), key=('enter'))],
        #[sg.Canvas(size=(150, 5))],
        #[sg.Canvas(size=(75, 0)), sg.Text(text='У Вас нет аккаунта?')],
        #[sg.Canvas(size=(62, 1), key=('cen_left_canvas2')),sg.Button(button_text=('Зарегистрироваться'), size=(17, 1), key=('register'))],
        #[sg.Canvas(size=(10, 0)), sg.Text(text='Ваш аккаунт создан, осталось войти в него!', key='complete_ok', visible=False)],
        #[sg.Canvas(size=(200, 25))]
    ]
    return sg.Window('Органайзер', layout, finalize=True)

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
# Для будущей версии, если найдем способ вывода многострочного текста в sg.Text
text_opros = 'Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации\n' \
             'Вам предлагается 25 утверждений, касающихся различных сторон Вашей жизни и способов обращения со временем. ' \
             'Введите в поле ту цифру, которая в наибольшей мере характеризует Вас и отражает Вашу точку зрения ' \
             '(1 — полное несогласие, 7 — полное согласие с данным утверждением, 4 — середина шкалы, остальные цифры — промежуточные значения'
count = 0
def make_after_login():
    layout = [  # Пресет после клика кнопки Войти
        [sg.Canvas(size=(1000, 2))],
        [sg.Canvas(size=(200, 30)),
         sg.Text(text='Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации')],
        [sg.Canvas(size=(1, 1)), sg.Text(
            text='Вам предлагается 25 утверждений, касающихся различных сторон Вашей жизни и способов обращения со временем. Введите в поле ту цифру, которая ')],
        [sg.Canvas(size=(1, 1)), sg.Text(
            text='в наибольшей мере характеризует Вас и отражает Вашу точку зрения (1 — полное несогласие, 7 — полное согласие с данным утверждением, 4 — середина ')],
        [sg.Canvas(size=(1, 1)), sg.Text(text='шкалы, остальные цифры — промежуточные значения)')],
        [sg.Canvas(size=(2, 10)), sg.Text(text=que[count], key=('opros')), sg.Input('', size=(2, 1), key=('input1'))],
        [sg.Canvas(size=(90, 1), key=('cen_left_canvas3')), sg.Button(button_text=('Далее'), size=(10, 1), key=('next'))],
        [sg.Canvas(size=(2, 10)), sg.Text('Баллы:'), sg.Text('', size=(3, 1), key=('sum'))],
        [sg.Canvas(size=(2, 5)), sg.Text(text='Введите значение от 1 до 7', visible=False, key=('mistake'))],
        [sg.Canvas(size=(90, 1), key=('cen_left_canvas3')),
         sg.Button(button_text=('Завершить'), size=(10, 1), key=('end'), visible=False)],
        [sg.Canvas(size=(1000, 5))]
    ]
    return sg.Window('Опрос', layout, finalize=True)

open = False

def make_register():
    layout = [
        [sg.Canvas(size=(500, 2))],
        [sg.Canvas(size=(200, 2)), sg.Text(text='Регистрация')],
        [sg.Canvas(size=(2, 10)), sg.Text(text='Введите фамилию  ', key=('surname')),
         sg.Input('', size=(20, 1), key=('input_sur'))],
        [sg.Canvas(size=(2, 10)), sg.Text(text='Введите имя          ', key=('name')),
         sg.Input('', size=(20, 1), key=('input_name'))],
        [sg.Canvas(size=(2, 10)), sg.Text(text='Введите отчество   ', key=('patronymic')),
         sg.Input('', size=(20, 1), key=('input_patr'))],
        [sg.Canvas(size=(2, 10)), sg.Text(text='Придумайте логин  ', key=('login')),
         sg.Input('', size=(20, 1), key=('input_login'))],
        [sg.Canvas(size=(2, 0)), sg.Text(text='Пароль должен содержать минимум 8 символов')],
        [sg.Canvas(size=(2, 0)), sg.Text(text='Придумайте пароль', key=('pass')),
         sg.Input('', size=(20, 0), key=('input_pass'), password_char='*'),
         sg.Button(button_text='      👁️', font='Arial, 12' ,size=(0, 0), key=('open_pass'))],
        [sg.Canvas(size=(2, 10)), sg.Text(text='Повторите пароль   ', key=('pass_check')),
         sg.Input('', size=(20, 1), key=('input_check'), password_char='*')],
        [sg.Canvas(size=(150, 50)),
         sg.Button(button_text=('Зарегистрироваться'), size=(20, 1), key=('reg_complete'))],
        [sg.Canvas(size=(2, 0)), sg.Text(text='Заполните все поля для завершения регистрации!', key='reg_check', visible=False)]
    ]
    return sg.Window('Регистрация', layout, finalize=True)

def make_rezult():
    layout = [
        [sg.Canvas(size=(500, 2))],
        [sg.Canvas(size=(180, 2)), sg.Text(text='Результаты опроса')],
        [sg.Canvas(size=(2, 2)), sg.Text(text='Количество набранных баллов: '),sg.Text('', size=(3, 1), key=('rez'))],
        [sg.Canvas(size=(180, 2)), sg.Text(text='', key=('rezt'))],
        [sg.Canvas(size=(150, 2)), sg.Button(button_text=('Завершить опрос'), size=(20, 1), key=('opros_complete'))]
    ]
    return sg.Window('Результаты', layout, finalize=True)

window = make_main_menu()
score = 0

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif 'enter' in event:
        cursor.execute('SELECT pass FROM USER_LOGIN_DATA where login = "' + values['input_main_login'] + '"')
        executed_str = ''.join(str(cursor.fetchone()))
        if executed_str == values['input_main_pass']:
            window.close()
            window = make_after_login()
        else:
            window.Element('error_mes').Update(visible=True)
    elif 'register' in event:
        window.close()
        window = make_register()
    elif 'next' in event:
        try:
            if int(values['input1']) > 7 or int(values['input1']) < 1:
                raise ValueError
            elif count == 0 or count == 4 or count == 9 or count == 14 or count == 20 or count == 22:
                if int(values['input1']) == 1:
                    score = score + 7           # Здесь рассматриваются варианты для утверждений с обратным рассчётом баллов
                if int(values['input1']) == 7:  # Например, указали 7 - программа берёт 1 и т.д.
                    score = score + 1
                if int(values['input1']) == 2:
                    score = score + 6
                if int(values['input1']) == 6:
                    score = score + 2
                if int(values['input1']) == 3:
                    score = score + 5
                if int(values['input1']) == 5:
                    score = score + 3
                if int(values['input1']) == 4:
                    score = score + 4
            else:
                score = score + int(values['input1'])
            window.Element('sum').Update(value=score)
            count = count + 1
            # Должно быть значение 25 (для тестов используем, например, 3)
            if count < 25:
                window.Element('mistake').Update(visible=False)
                window.Element('opros').Update(value=que[count])
                window.Element('input1').Update(value='')
                # Должно быть значение 24 (для тестов используем, например, 2)
                if count == 24:
                    window.Element('next').Update(visible=False)
                    window.Element('end').Update(visible=True)
        except:
            window.Element('mistake').Update(visible=True)
            window.Element('input1').Update(value='')
            window.Element('sum').Update(value=score)
    elif 'end' in event:
        if values['input1']!= '':
            score = score + int(values['input1'])
        window.close()
        window = make_rezult()
        window.Element('rez').Update(value=score)
        if 0 < score < 59:
            window.Element('rezt').Update(value='Ваш уровень самоорганизации низкий.')
        if 58 < score < 117:
            window.Element('rezt').Update(value='Ваш уровень самоорганизации средний.')
        if 116 < score < 176:
            window.Element('rezt').Update(value='Ваш уровень самоорганизации высокий.')
    elif 'open_pass' in event:
        if open:
            open = False
            window.Element('input_pass').Update(password_char='*')
        else:
            open = True
            window.Element('input_pass').Update(password_char='')
    elif 'reg_complete' in event:
        if (values['input_sur'] or values['input_name'] or values['input_patr'] or values['input_login'] or values['input_pass'] or values['input_check']) == '':
            window.Element('reg_check').Update(value='Заполните все поля для завершения регистрации!',visible=True)
        elif values['input_pass'] != values['input_check']:
            window.Element('reg_check').Update(value='Пароли не совпадают!', visible=True)
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
        window = make_main_menu()
window.close()
