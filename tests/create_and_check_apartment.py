import json
import random
import time

import logs


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


def create_random_params_for_apart(apart_id):
    """
    Creating dict for apartments menu with random values
    :param apart_id: apartment id
    :return: data to send with POST or PUT request
    """
    result = {'id': str(apart_id),
              'sip': {'enabled': random_bool(),
                      'video_call': random_bool(),
                      'phone_numbers': random_list(5, 5, 3, 20),  # TODO make random length of string
                      'analog': random_bool(),
                      'call_method': str(random.choice([1, 2, 3]))},
              'access_code': get_random_string(length_min=4, length_max=6, sample_letters='0123456789'),
              'door_access': random_doors(),
              'rfids': random_list(5, 5, 3, 20),
              'notification': random_bool()}
    return result


def create_apartment(io_object, apart_id, apart_data_for_post, apart_data_for_put):
    """
    Sending 4 requests with delay: GET -> DELETE (if get returns 200 code) -> POST(apart_data_for_post) ->
    -> PUT(apart_data_for_put) -> GET
    :param io_object: WebApiAdapter from main.py
    :param apart_id: apartment number
    :param apart_data_for_post:
    :param apart_data_for_put:
    :return: last GET response
    """
    time_between_requests = 0.01

    response = io_object.send_request_hard(method='GET', api_menu='apartments', index=str(apart_id),
                                           data=None)
    time.sleep(time_between_requests)

    if response.status_code in [200, 201, 202, 203]:
        io_object.send_request_hard(method='DELETE', api_menu='apartments', index=str(apart_id),
                                    data=None)
        time.sleep(time_between_requests)
    else:
        pass

    io_object.send_request_hard(method='POST', api_menu='apartments', index=str(apart_id),
                                data=json.dumps(apart_data_for_post))
    time.sleep(time_between_requests)

    io_object.send_request_hard(method='PUT', api_menu='apartments', index=str(apart_id), data=json.dumps(
        apart_data_for_put))
    time.sleep(time_between_requests)

    response = io_object.send_request_hard(method='GET', api_menu='apartments', index=str(apart_id),
                                           data=None)
    time.sleep(time_between_requests)
    return response


def test_main(io_object):
    """
    Creating list for apartments segment with random data. Doing function create_apartment for this list.
    Than deleting all created apartments
    :param io_object:WebApiAdapter from main.py
    :return: True is test succeeded
    """
    list_of_apart_data = []
    apartment_from = 1
    apartment_to = 50
    apartment_list = range(apartment_from, apartment_to)
    for apart_id in apartment_list:
        list_of_apart_data.append(
            (apart_id, create_random_params_for_apart(apart_id),
             create_random_params_for_apart(apart_id)))  # creating list of tuples (id, json_1, json_2)

    for i in list_of_apart_data:
        response = create_apartment(io_object, i[0], apart_data_for_post=i[1], apart_data_for_put=i[2])
        # TODO сделать проверку соответсвия последнего GET с PUT

    logs.logger.info(f'Apartments from {apartment_from} to {apartment_to} set. Starting to Delete...')

    for apart_id in apartment_list:
        io_object.send_request_hard(method='DELETE', api_menu='apartments', index=str(apart_id),
                                    data=None)
    logs.logger.info(f'Apartments deleted')
    return True
