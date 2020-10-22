import random


def random_bool():
    """
    :return: random boolean value
    """
    boolean = random.choice([0, 1])
    if boolean == 1:
        result = True
    else:
        result = False
    return result


def random_list(list_length_min, list_length_max, length_min, length_max):
    """
    Creating list with length in (min - max) and random values with length (min-max) from func get_random_string()
    :param list_length_min: minimum list length
    :param list_length_max: maximum list length
    :param length_min: minimum value length
    :param length_max: maximum value length
    :return: random list
    """
    list_length = random.choice(range(list_length_min, list_length_max + 1))
    result = []
    for i in range(list_length):
        result.append(get_random_string(length_min, length_max))
    return result


def get_random_string(length_min, length_max, sample_letters='abcdefghijklmnopqrstuvwxyz1234567890'):
    """
    :param length_min: minimum value length
    :param length_max: maximum value length
    :param sample_letters: list of values to generate from
    :return: random string
    """
    length = random.choice(range(length_min, length_max))
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


def random_doors():
    """
    Creating list with random ints (0-7) and random length, then shuffle it
    :return:
    """
    result = []
    for i in range(7):
        rand = random.choice([0, 1])
        if rand == 1:
            result.append(i)
        elif rand == 0:
            pass
    random.shuffle(result)
    return result
