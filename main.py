import PySimpleGUI as sg

layout_main_menu = [              #Начальный пресет
   [sg.Canvas(size=(150,10))],
   [sg.Canvas(size=(80,0)), sg.Text(text='Добро пожаловать!')],
   [sg.Canvas(size=(55,0)), sg.Text(text='Вас приветствует органайзер')],
   [sg.Canvas(size=(0,0)), sg.Text(text='Введите логин  '),sg.InputText(size=(20,1))],
   [sg.Canvas(size=(150,5))],
   [sg.Canvas(size=(0,0)), sg.Text(text='Введите пароль'),sg.InputText(size=(20,1))],
   [sg.Canvas(size=(150,15))],
   [sg.Canvas(size=(90,1), key=('cen_left_canvas')), sg.Button(button_text=('Войти'), size=(10,1), key=('cen_button'))],
   [sg.Canvas(size=(150,5))],
   [sg.Canvas(size=(75,0)), sg.Text(text='У Вас нет аккаунта?')],
   [sg.Canvas(size=(62,1), key=('cen_left_canvas')), sg.Button(button_text=('Зарегистрироваться'), size=(17,1), key=('cen_button1'))],
   [sg.Canvas(size=(280, 25))]
]

layout_after_login = [            #Пресет после клика кнопки Войти
   [sg.Canvas(size=(280,100))],
   [sg.Canvas(size=(60,1)), sg.Text(text='Для начала работы Вам необходимо пройти опрос \nна определение Вашего уровня самоорганизации')],
   [sg.Canvas(size=(280, 100))]
]
window = sg.Window('PSA', layout_main_menu)

#def runCommand():

 #  pass
while True:
   event, values = window.Read()
   if event in (None, sg.WIN_CLOSED):
    break
    if event == 'Войти':
       window = sg.Window('PSA', layout_after_login)
       #runCommand()

      # window = sg.Window('PSA', layout_after_login)
