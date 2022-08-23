from cmath import sqrt
from pynput.keyboard import Key, Controller
from time import sleep
from random import uniform as randfloat, randint
from keyboard import wait as kb_wait, is_pressed
from PIL import Image as pil_image
from colorama import init, Fore, Back, Style
from json import dump, loads
from shutil import get_terminal_size
from pytesseract import image_to_string, pytesseract as tsr
from os import remove as delete_file, getcwd as getDirPath
from os.path import exists as file_exists

import pyautogui as pygui

init()

keyboard = Controller()

print(Back.RED + 'KLAVAGONKI CHEAT'.center(get_terminal_size().columns, ' ') + Style.RESET_ALL + '\n')

print('Создатель: Лукьянов Виктор из группы 20ОКС1'.center(get_terminal_size().columns))
print('Программа скаммит мамонтов на сайте клавогонок'.center(get_terminal_size().columns))

print(Fore.GREEN + 'Инструкция'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')

print(Fore.RED + 'Предварительно установи pytesseract на пекарню, иначе не попрет брат. В архиве установочник.'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')

print('Чтобы активировать бота и включить его функции, либо перезапустить после работы - нажми кнопку активации'.center(get_terminal_size().columns))
print('Когда бот активен - выбери где текст начинается (чуть левее и выше от него) и нажми кнопку выбора точки'.center(get_terminal_size().columns))
print('Повтори то же самое с концом текста (только правее и ниже)'.center(get_terminal_size().columns))
print('Нажми на текстовое поле, чтобы оно было активно'.center(get_terminal_size().columns))
print('Жди несколько секунд и бот заскаммит мамонтов'.center(get_terminal_size().columns))
print('Чтобы экстренно остановить бота - жми кнопку остановки во время работы'.center(get_terminal_size().columns))

print(Fore.RED + 'P.S Пусть только кто-то из 20ОКС2 попробует воспользоваться этой прогой - у вас на комьютере будут майниться биткоины для меня.'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')

# Иногда спасает, когда бот неправильно видит символы.

normalWords = {}

normalWords['«'] = '"'
normalWords['»'] = '"'
normalWords['—-'] = '-'
normalWords['-—'] = '-'
normalWords['——'] = '-'
normalWords['--'] = '-'
normalWords['- -'] = '-'
normalWords['— —'] = '-'
normalWords['— -'] = '-'
normalWords['- —'] = '-'
normalWords['—'] = '-'
normalWords['  '] = ' '
normalWords['\n'] = ' '

if not file_exists('settings.json'):
    settingsBot = {}

    settingsBot['wait_Min'] = 0.15
    settingsBot['wait_Max'] = 0.6
    settingsBot['wait_OnError_Min'] = 0.3
    settingsBot['wait_OnError_Max'] = 0.7
    settingsBot['wait_Before_Write'] = 1
    settingsBot['wait_keyRelease'] = 0.025
    settingsBot['error_Chance_Percent'] = 4
    settingsBot['enabled_Languages'] = 'rus'
    settingsBot['points_Select_Key'] = 'f4'
    settingsBot['activate_Bot'] = 'insert'
    settingsBot['stop_Bot'] = 'esc'
    settingsBot['show_Settings_On_StartUp'] = True
    
    with open('settings.json', 'w+') as settingsFile:
        dump(settingsBot, settingsFile, indent = 6)
        settingsFile.close()
    
else:
    with open('settings.json', 'r+') as settingsFile:
        settingsBot = loads(settingsFile.read())
        settingsFile.close()
    
if settingsBot['show_Settings_On_StartUp']:
    wait_conc = str(settingsBot['wait_Min']) + ' s. / ' + str(settingsBot['wait_Max']) + ' s.'
    wait_error_conc = str(settingsBot['wait_OnError_Min']) + ' s. / ' + str(settingsBot['wait_OnError_Max']) + ' s.'
    wait_release = str(settingsBot['wait_keyRelease']) + ' s.'
    error_Chance = str(settingsBot['error_Chance_Percent']) + '%'
    wait_before = str(settingsBot['wait_Before_Write']) + ' s. '
    langs = settingsBot['enabled_Languages'].replace('+', ' ')
    pointsKey = settingsBot['points_Select_Key']
    activateKey = settingsBot['activate_Bot']
    stopKey = settingsBot['stop_Bot']
        
    print(Fore.GREEN + 'Настройки (изменять в settings.json):'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')
    print(f'Минимальная/Максимальная задержка при печати: {wait_conc}'.center(get_terminal_size().columns))
    print(f'Минимальная/Максимальная задержка при ошибках: {wait_error_conc}'.center(get_terminal_size().columns))
    print(f'Время до того, как бот отпустит нажатую клавишу: {wait_release}'.center(get_terminal_size().columns))
    print(f'Шанс ошибки в процентах: {error_Chance}'.center(get_terminal_size().columns))
    print(f'Задержка перед началом печати: {wait_before}'.center(get_terminal_size().columns))
    print(f'Подключенные языки: {langs}'.center(get_terminal_size().columns))
    print(f'Кнопка выбора точек: {pointsKey}'.center(get_terminal_size().columns))
    print(f'Кнопка активации: {activateKey}'.center(get_terminal_size().columns))
    print(f'Кнопка остановки: {stopKey}'.center(get_terminal_size().columns))

print('\n')

def findLengthVector(x1, y1, x2, y2):
        
    skobka_f = pow((x2 - x1), 2)
    skobka_s = pow((y2 - y1), 2)
        
    underSqr = sqrt(skobka_f + skobka_s)
        
    return round(underSqr.real)

def pressEmul(button, waitMin = None, waitMax = None):
    
    if waitMin != None and waitMax != None:
        sleep(randfloat(waitMin, waitMax))
    else: 
        sleep(randfloat(settingsBot['wait_Min'], settingsBot['wait_Max']))
    
    keyboard.press(button)
    sleep(settingsBot['wait_keyRelease'])
    keyboard.release(button)

def activateBot():

    kb_wait(settingsBot['points_Select_Key'])
    fposX, fposY = pygui.position()
    print(f'ПЕРВЫЕ ПОЗИЦИИ: {fposX} , {fposY}')

    kb_wait(settingsBot['points_Select_Key'])
    sposX, sposY = pygui.position()
    print(f'ВТОРЫЕ ПОЗИЦИИ: {sposX} , {sposY}\n\n')

    img = pygui.screenshot(region=(fposX, fposY, findLengthVector(fposX, 0, sposX, 0), findLengthVector(0, fposY, 0, sposY)))
    img.save('suka.jpg')

    tsr.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    img = pil_image.open('suka.jpg')
    
    text = image_to_string(img, lang = 'rus', config = '-l {0} --psm 6 --oem 3'.format(settingsBot['enabled_Languages']))
    text = text.strip()
    
    delete_file(getDirPath() + r'\suka.jpg')
    
    for s in normalWords:
        while s in text:
            if s == '\n':
                print(Fore.RED + Back.YELLOW + 'Заменил символ: [ОТСТУП] --> [ПРОБЕЛ]' + Style.RESET_ALL + '\n\n')
            else:
                print(Fore.RED + Back.YELLOW + f'Заменил символ: {s} --> {normalWords[s]}' + Style.RESET_ALL + '\n\n')
            text = text.replace(s, normalWords[s])
            
    while '  ' in text:
        print(Fore.RED + Back.YELLOW + 'Заменил символ: [2х ПРОБЕЛ] --> [ПРОБЕЛ]' + Style.RESET_ALL + '\n\n')
        text = text.replace('  ', ' ')

    print(Fore.YELLOW + f'Прочитал текст: {text}' + Style.RESET_ALL + '\n\n')

    sleep(settingsBot['wait_Before_Write'])
        
    textWhileWork = ''
        
    for w in text:
        
        if is_pressed(settingsBot['stop_Bot']):
            print(Back.RED + f'Пользователь прервал работу бота!'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')
            return
        
        if settingsBot['error_Chance_Percent'] > 0:
            needNumber = 100 / settingsBot['error_Chance_Percent']
            needError = randint(1, needNumber)
            
            if needError == needNumber: 
                
                if w == '.' or w == ',':
                    pressEmul('Ю')
                    pressEmul(Key.backspace, settingsBot['wait_OnError_Min'], settingsBot['wait_OnError_Max'])
                    print(Fore.RED + Back.YELLOW + f'Специальная ошибка допущена: точка --> Ю.' + Style.RESET_ALL + '\n\n')
                
                elif textWhileWork != '': 
                    pressEmul(textWhileWork[len(textWhileWork) - 1])
                    pressEmul(Key.backspace, settingsBot['wait_OnError_Min'], settingsBot['wait_OnError_Max'])
                    print(Fore.RED + Back.YELLOW + f'Специальная ошибка допущена: повторение нажатой буквы.' + Style.RESET_ALL + '\n\n')
        
        textWhileWork += w
        pressEmul(w)
    
    print(Back.GREEN + f'Бот закончил свою работу!'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')
    
while True:
    kb_wait(settingsBot['activate_Bot'])
    print(Back.GREEN + f'Бот готов к использованию!'.center(get_terminal_size().columns) + Style.RESET_ALL + '\n')
    activateBot()