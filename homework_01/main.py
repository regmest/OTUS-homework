"""
Домашнее задание №1
Функции и структуры данных
"""

"""
функция, которая принимает N целых чисел,
и возвращает список квадратов этих чисел
"""
def power_numbers(*number):
    return [i ** 2 for i in number]

"""
функция, которая на вход принимает список из целых чисел,
и возвращает только чётные/нечётные/простые числа
(выбор производится передачей дополнительного аргумента)
"""
# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"

def is_prime(num):
    division_cnt = 0
    for i in range(2, num):
        if num % i == 0:
            division_cnt += 1
    if division_cnt == 0 and num > 1:
        return True

def filter_numbers(number_list, filter_type=PRIME):
    even_numbers = [i for i in number_list if i % 2 == 0]
    if filter_type == PRIME:
        return list(filter(is_prime, number_list))
    elif filter_type == EVEN:
        return even_numbers
    else:
        return [i for i in number_list if i not in even_numbers]
