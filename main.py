import PySimpleGUI as sg
#import re
layout_main_menu = [              #Начальный пресет
   [sg.Canvas(size=(150,10))],
   [sg.Canvas(size=(80,0)), sg.Text(text='Добро пожаловать!')],
   [sg.Canvas(size=(55,0)), sg.Text(text='Вас приветствует органайзер')],
   [sg.Canvas(size=(0,0)), sg.Text(text='Введите логин  '),sg.InputText(size=(20,1))],
   [sg.Canvas(size=(150,5))],
   [sg.Canvas(size=(0,0)), sg.Text(text='Введите пароль'),sg.InputText(size=(20,1))],
   [sg.Canvas(size=(150,15))],
   [sg.Canvas(size=(90,1), key=('cen_left_canvas1')), sg.Button(button_text=('Войти'), size=(10,1), key=('enter'))],
   [sg.Canvas(size=(150,5))],
   [sg.Canvas(size=(75,0)), sg.Text(text='У Вас нет аккаунта?')],
   [sg.Canvas(size=(62,1), key=('cen_left_canvas2')), sg.Button(button_text=('Зарегистрироваться'), size=(17,1), key=('register'))],
   [sg.Canvas(size=(280, 25))]
]
que = [ #Массив строк для опроса
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
count=0
layout_after_login = [            #Пресет после клика кнопки Войти
   [sg.Canvas(size=(1000,2))],
   [sg.Canvas(size=(200,30)), sg.Text(text='Для начала работы Вам необходимо пройти опрос на определение Вашего уровня самоорганизации')],
   [sg.Canvas(size=(1,1)), sg.Text(text='Вам предлагается 25 утверждений, касающихся различных сторон Вашей жизни и способов обращения со временем. Введите в поле ту цифру, которая ')],
   [sg.Canvas(size=(1,1)), sg.Text(text='в наибольшей мере характеризует Вас и отражает Вашу точку зрения (1 — полное несогласие, 7 — полное согласие с данным утверждением, 4 — середина ')],
   [sg.Canvas(size=(1,1)), sg.Text(text='шкалы, остальные цифры — промежуточные значения)')],
   [sg.Canvas(size=(2,10)), sg.Text(text=que[count], key=('opros')), sg.Input('', size=(2,1),key = ('input1'))],
   [sg.Canvas(size=(90,1), key=('cen_left_canvas3')), sg.Button(button_text=('Далее'), size=(10,1), key=('next'))],
   [sg.Canvas(size=(2,10)), sg.Input('', size=(3,1),key = ('sum'))],
   [sg.Canvas(size=(2,5)), sg.Text(text='Введите значение от 1 до 7', visible=False, key=('mistake'))],
   [sg.Canvas(size=(1000, 5))]
]
layout_register = [
   [sg.Canvas(size=(500,2))],
   [sg.Canvas(size=(200,2)), sg.Text(text='Регистрация')],
   [sg.Canvas(size=(2,10)), sg.Text(text='Введите фамилию', key=('surname')), sg.Input('',size=(20,1), key=('input3'))],
   [sg.Canvas(size=(2,10)), sg.Text(text='Введите имя', key=('name')), sg.Input('',size=(20,1), key=('input2'))],
   [sg.Canvas(size=(2,10)), sg.Text(text='Введите отчество', key=('otch')), sg.Input('',size=(20,1), key=('input4'))],
   [sg.Canvas(size=(2,10)), sg.Text(text='Придумайте логин', key=('login')), sg.Input('',size=(20,1), key=('input5'))],
   [sg.Canvas(size=(2,10)), sg.Text(text='Придумайте пароль', key=('password')), sg.Input('',size=(20,1), key=('input6'))],
   [sg.Canvas(size=(2,0)), sg.Text(text='Пароль должен содержать минимум 8 символов')],
   [sg.Canvas(size=(2,10)), sg.Text(text='Повторите пароль', key=('password1')), sg.Input('',size=(20,1), key=('input7'))]
]
window = sg.Window('Органайзер', layout_main_menu)
sum=0
while True:
   event, values = window.Read()
   if event in (None, sg.WIN_CLOSED):
    break
   elif 'enter' in event:
      window.close()
      window = sg.Window('Опрос', layout_after_login)
   elif 'next' in event:
      try:
         if int(values['input1']) > 7 or int(values['input1']) < 1:
            raise ValueError
         elif count == 0 or count == 4 or count == 9 or count == 14 or count == 20 or count == 22:
            if int(values['input1']) == 1:
               sum=sum+7                                     #Здесь рассматриваются варианты для утверждений с обратным рассчётом баллов
            if int(values['input1']) == 7:                   #Например, указали 7 - программа берёт 1 и т.д.
               sum=sum+1
            if int(values['input1']) == 2:
               sum=sum+6
            if int(values['input1']) == 6:
               sum=sum+2
            if int(values['input1']) == 3:
               sum=sum+5
            if int(values['input1']) == 5:
               sum=sum+3
            if int(values['input1']) == 4:
               sum=sum+4
            window.Element('sum').Update(value=sum)
            count=count+1
            window.Element('mistake').Update(visible=False)
            window.Element('opros').Update(value=que[count])
            window.Element('input1').Update(value='')
         else:
            sum=sum+int(values['input1'])
            window.Element('sum').Update(value=sum)
            count=count+1
            window.Element('mistake').Update(visible=False)
            window.Element('opros').Update(value=que[count])
            window.Element('input1').Update(value='')
      except:
         window.Element('mistake').Update(visible=True)
         window.Element('input1').Update(value='')
   elif 'register' in event:         #Регистрация
      window.close()
      window = sg.Window('Регистрация',layout_register)






