import re

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
        [sg.Text('Введите логин   ', font=fonts[1]),
         sg.InputText(size=(20, 1), key='input_main_login')],
        [sg.Text('Введите пароль', font=fonts[1]),
         sg.InputText(size=(20, 1), key='input_main_pass', password_char='*')],
        [sg.Button(button_text=('Войти'), size=(20, 1), key=('enter'))],
        [sg.Text('У Вас нет аккаунта?', font=fonts[1])],
        [sg.Button(button_text=('Зарегистрироваться'), size=(30, 1), key=('register'))],
        [sg.Text('*Ваш аккаунт создан, осталось войти в него!', font=fonts[1], key='complete_ok', visible=False)],
    ]
    return sg.Window('Органайзер', layout, icon=r'1.ico', size=(500, 250), resizable=True, finalize=True, grab_anywhere=True, element_justification='c')

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
        [sg.Text(text='Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации', font=fonts[0])],
        [sg.Text(
            text='Вам предлагается 25 утверждений, касающихся различных сторон Вашей жизни и способов обращения со временем. Введите в поле ту цифру, которая ', font=fonts[1])],
        [sg.Text(
            text='в наибольшей мере характеризует Вас и отражает Вашу точку зрения (1 — полное несогласие, 7 — полное согласие с данным утверждением, 4 — середина ', font=fonts[1])],
        [sg.Text(text='шкалы, остальные цифры — промежуточные значения)', font=fonts[1])],
        [sg.Text(text=que[count], key=('opros'), font=fonts[1]), sg.Slider(range=(1,7), orientation='horizontal', tick_interval=1, default_value=4, key='input1')],
        [sg.Button(button_text=('Далее'), size=(10, 1), key=('next'))],
        [sg.Text('Баллы:'), sg.Text('', size=(3, 1), key=('sum'), font=fonts[1])],
        [sg.Button(button_text=('Завершить'), size=(10, 1), key=('end'), visible=False)]
    ]
    return sg.Window('Опрос', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='c')

open = False

def make_register():
    layout = [     #[sg.Text('Enter the value',justification='center',size=(100,1))],
        [sg.Text('Регистрация', font=fonts[0])],
        [sg.Text('Введите фамилию   ', font=fonts[1], key=('surname')), sg.Input('', size=(40, 1), key=('input_sur'))],
        [sg.Text('Введите имя            ', font=fonts[1], key=('name')), sg.Input('', size=(40, 1), key=('input_name'))],
        [sg.Text('Введите отчество   ', font=fonts[1], key=('patronymic')), sg.Input('', size=(40, 1), key=('input_patr'))],
        [sg.Text('Придумайте логин   ', font=fonts[1], key=('login')), sg.Input('', size=(40, 1), key=('input_login'))],
        [sg.Text('Придумайте пароль', font=fonts[1], key=('pass')), sg.Input('', size=(28, 1), key=('input_pass'), password_char='*'), sg.Button(button_text='      👁️', font=fonts[1], key=('open_pass'))],
        [sg.Text('Повторите пароль   ', font=fonts[1], key=('pass_check')), sg.Input('', size=(40, 1), key=('input_check'), password_char='*')],
        [sg.Text('*Пароль должен содержать минимум 8 символов', font=fonts[1])],
        [sg.Button(button_text=('Зарегистрироваться'), size=(20, 1), key=('reg_complete'))],
        [sg.Text('Заполните все поля для завершения регистрации!', font=fonts[1], key='reg_check', visible=False)]
    ]
    return sg.Window('Регистрация', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='c')

def make_rezult():
    layout = [
        [sg.Text(text='Результаты опроса', font=fonts[0])],
        [sg.Text(text='Количество набранных баллов: '),sg.Text('', size=(3, 1), key=('rez'), font=fonts[1])],
        [sg.Text(text='', key=('rezt'), font=fonts[1])],
        [sg.Button(button_text=('Завершить опрос'), size=(20, 1), key=('opros_complete'))]
    ]
    return sg.Window('Результаты', layout, resizable=True, finalize=True, grab_anywhere=True, element_justification='c')

window = make_main_menu()
score = 0

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif 'enter' in event:
        cursor.execute('SELECT pass FROM USER_LOGIN_DATA where login = "' + values['input_main_login'] + '"')
        executed_str = ''.join(str(cursor.fetchone()))
        executed_str = re.sub("[^A-Za-z0-9]", "", executed_str)
        if executed_str == values['input_main_pass']:
            window.close()
            window = make_after_login()
        else:
            window.Element('error_mes').Update(visible=True)
    elif 'register' in event:
        window.close()
        window = make_register()
    elif 'next' in event:
        if count == 0 or count == 4 or count == 9 or count == 14 or count == 20 or count == 22:
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
            window.Element('opros').Update(value=que[count])
            window.Element('input1').Update(value='')
            # Должно быть значение 24 (для тестов используем, например, 2)
            if count == 24:
                window.Element('next').Update(visible=False)
                window.Element('end').Update(visible=True)
    elif 'end' in event:
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
        window = make_main_menu()
window.close()
