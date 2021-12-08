import PySimpleGUI as sg

layout_main_menu = [              #Начальный пресет
   [sg.Canvas(size=(150,10))],
   [sg.Canvas(size=(80,0)), sg.Text(text='Добро пожаловать!')],
   [sg.Canvas(size=(55,0)), sg.Text(text='Вас приветствует органайзер')],
   [sg.Canvas(size=(0,0)), sg.Text(text='Введите логин  '),sg.InputText(size=(20,1))],
   [sg.Canvas(size=(150,5))],
   [sg.Canvas(size=(0,0)), sg.Text(text='Введите пароль'),sg.InputText(size=(20,1))],
   [sg.Canvas(size=(150,15))],
   [sg.Canvas(size=(90,1), key=('cen_left_canvas')), sg.Button(button_text=('Войти'), size=(10,1), key=('enter'))],
   [sg.Canvas(size=(150,5))],
   [sg.Canvas(size=(75,0)), sg.Text(text='У Вас нет аккаунта?')],
   [sg.Canvas(size=(62,1), key=('cen_left_canvas')), sg.Button(button_text=('Зарегистрироваться'), size=(17,1), key=('register'))],
   [sg.Canvas(size=(280, 25))]
]

layout_after_login = [            #Пресет после клика кнопки Войти
   [sg.Canvas(size=(1000,2))],
   [sg.Canvas(size=(50,1)), sg.Text(text='Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации')],
   [sg.Canvas(size=(1,10)), sg.Text(text='Вам предлагается ряд утверждений, касающихся \nразличных сторон Вашей жизни и способов обращения \nсо временем. Введите в поле ту цифру, которая в \nнаибольшей мере характеризует \nВас и отражает Вашу точку зрения (1 — полное несогласие, \n7 — полное согласие с данным утверждением, 4 — \nсередина шкалы, остальные цифры — промежуточные значения). ')],
   [sg.Canvas(size=(2,10)), sg.Text(text='1. Мне требуется много времени, чтобы “раскачаться” и начать действовать'), sg.Input('0', size=(2,1),key = ('input1'))],
   [sg.Canvas(size=(1000, 5))]
]
window = sg.Window('Органайзер', layout_main_menu)
while True:
   event, values = window.Read()
   if event in (None, sg.WIN_CLOSED):
    break
   elif 'enter' in event:
      window.close()
      window = sg.Window('Опрос', layout_after_login)




