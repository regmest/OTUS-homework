"""
Домашнее задание №1
Функции и структуры данных
"""


def power_numbers(*number):
    """
    функция, которая принимает N целых чисел,
    и возвращает список квадратов этих чисел
    """

    return [i ** 2 for i in number]


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
    """
    функция, которая на вход принимает список из целых чисел,
    и возвращает только чётные/нечётные/простые числа
    (выбор производится передачей дополнительного аргумента)
    """

    if filter_type == PRIME:
        return list(filter(is_prime, number_list))
    elif filter_type == EVEN:
        return [i for i in number_list if i % 2 == 0]
    else:
        return [i for i in number_list if i % 2 != 0]

