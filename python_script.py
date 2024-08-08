#!/usr/bin/env python3
import os
from pynput.keyboard import Key, Listener


# Функция для получения размера папки рекурсивно
def folder_size(path='.'):
    total_size = 0
    for item in os.scandir(path):
        if item.is_file():
            total_size += item.stat().st_size
        elif item.is_dir():
            total_size += folder_size(item.path)
    return total_size


# Функция для печати таблицы с информацией о файлах/папках
def print_table(data, start=0, end=9):
    # расчёт максимальной длинны колонок
    max_columns = []  # список максимальной длинны колонок
    for col in tuple(zip(*data[start:end+1]))[:-1]:
        len_el = []
        for el in col:
            len_el.append(len(el))
        max_columns.append((max(len_el)))
    # печать шапки таблицы
    for n, col in enumerate(["Имя", "Размер"]):
        print(f'{col:{max_columns[n]+1}}', end='')
    print()
    # печать разделителя шапки '='
    print('=' * sum(max_columns))
    # печать тела таблицы
    for el in data[start:end+1]:
        for n, col in enumerate(el[:-1]):
            # выравнвание по правому краю >
            print(f'{col:{max_columns[n]+1}}', end='')
        print()
    print('=' * sum(max_columns))


# Функция для преобразования размера в КБ, МБ, ГБ
def convert_size(size_bytes):
    if 999 < size_bytes < 1000000:
        result = size_bytes / 1000
        return f'{result:.2f} KB'
    elif 1000000 < size_bytes < 1000000000:
        result = size_bytes / 1000000
        return f'{result:.2f} MB'
    elif size_bytes > 1000000000:
        result = size_bytes / 1000000000
        return f'{result:.2f} GB'
    else:
        return str(size_bytes) + ' B'


def pressed(key):
    global start, end
    # print('Pressed:', key)
    if key == Key.up:
        start -= 10
        if start < 0:
            start = 0
        end = start + 10
        print_table(item_info, start, end)
        if start == 0:
            print('Начало таблицы')
        print('Чтобы посмотреть таблицу нажимайте стрелки вверх и вниз', 'ESC - выход', sep='\n')
    if key == Key.down:
        start += 10
        if start > len(item_info) - 10:
            start = len(item_info) - 10
        end = start + 10
        print_table(item_info, start, end)
        if end == len(item_info):
            print('Конец таблицы')
        print('Чтобы посмотреть таблицу нажимайте стрелки вверх и вниз', 'ESC - выход', sep='\n')


def released(key):
    # print('Released:', key)
    if key == Key.esc:
        return False


# Получаем текущую директорию
cur_dir = os.getcwd()
# Получаем список файлов в текущей директории
items = os.scandir(cur_dir)
# Список для хранения информации о каждом файле/папке
item_info = []
# Пробегаемся по списку и добавляем информацию о каждом файле/папке
for item in items:
    info = []
    info.append(item.name)
    if item.is_file():
        f_size = item.stat().st_size
    elif item.is_dir():
        f_size = folder_size(item.path)
    info.append(convert_size(f_size))
    info.append(f_size)
    item_info.append(info)
# Сортируем список с информацией о файлах/папках по размеру
item_info.sort(key=lambda x: x[2], reverse=True)
# Выводим информацию о каждом файле/папке
print()
print('Информация о файлах/папках в директории:', cur_dir)
# Печаем таблицу с информацией о файлах/папках
start = 0
end = 10
print_table(item_info, start, end)
print('Чтобы посмотреть таблицу нажимайте стрелки вверх и вниз', 'ESC - выход', sep='\n')
# Цикл для обнаружения нажатия клавиш, который выполняется до тех пор, пока не будет нажата клавиша escape
with Listener(on_press=pressed, on_release=released) as detector:
    detector.join()
