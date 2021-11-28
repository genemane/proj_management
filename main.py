import PySimpleGUI as sg
layout_main_menu = [           #Начальный пресет
    [sg.Canvas(size=(300,100), key=('upper_canvas'))],
    [sg.Canvas(size=(90,1), key=('cen_left_canvas')), sg.Button(button_text=('Войти'), size=(10,1), key=('cen_button'))],
    [sg.Canvas(size=(300, 100), key=('down_canvas'))]
]
layout_after_login = [         #Пресет после клика кнопки Войти
    [sg.Canvas(size=(300,100))],
    [sg.Canvas(size=(60,1)), sg.Text(text='Введите логин'),sg.InputText(size=(20,1))],
    [sg.Canvas(size=(300, 100))]
]
window = sg.Window('PSA', layout_main_menu)
while True:
    event, values = window.read()
    if event in (None, 'Далее', 'Закрыть'):
        break
    if event == 'Войти':
        break                    #Тут короче функция должна быть для смены пресета набора объектов,
                                 #но я пока не разобрался
