import json
import random
import time

import logs


def random_bool():
    boolean = random.choice([0, 1])
    if boolean == 1:
        result = True
    else:
        result = False
    return result


def random_list(list_length, value_length):
    result = []
    for i in range(list_length):
        result.append(get_random_string(value_length))
    return result


def get_random_string(length, sample_letters='abcdefghijklmnopqrstuvwxyz1234567890'):
    # put your letters in the following string
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


def random_doors():
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
    result = {'id': str(apart_id),
              'sip': {'enabled': random_bool(),
                      'video_call': random_bool(),
                      'phone_numbers': random_list(5, 8),  # TODO make random length of string
                      'analog': random_bool(),
                      'call_method': str(random.choice([1, 2, 3]))},
              'access_code': get_random_string(length=4, sample_letters='0123456789'),
              'door_access': random_doors(),
              'rfids': random_list(5, 8),
              'notification': random_bool()}
    return result


def create_apartment(io_object, apart_id, apart_data_for_post, apart_data_for_put):
    time_between_requests = 0.01

    response = io_object.send_request_hard(method='GET', api_menu='apartments', index=str(apart_id),
                                           data=None)  # check apart is exist, show params
    time.sleep(time_between_requests)

    if response.status_code in [200, 201, 202, 203]:
        io_object.send_request_hard(method='DELETE', api_menu='apartments', index=str(apart_id),
                                    data=None)  # creating deleting apart if it exist
        time.sleep(time_between_requests)
    else:
        pass

    io_object.send_request_hard(method='POST', api_menu='apartments', index=str(apart_id),
                                data=json.dumps(apart_data_for_post))  # creating apart
    time.sleep(time_between_requests)

    io_object.send_request_hard(method='PUT', api_menu='apartments', index=str(apart_id), data=json.dumps(
        apart_data_for_put))  # changing apart with same data? TODO может стоить менять его другой датой?

    time.sleep(time_between_requests)

    response = io_object.send_request_hard(method='GET', api_menu='apartments', index=str(apart_id),
                                           data=None)  # check apart is exist
    time.sleep(time_between_requests)
    return response


def test_main(io_object):
    list_of_apart_data = []
    for apart_id in range(1, 50):
        list_of_apart_data.append(
            (apart_id, create_random_params_for_apart(apart_id),
             create_random_params_for_apart(apart_id)))  # creating list of tuples (id, json)

    for i in list_of_apart_data:
        responce = create_apartment(io_object, i[0], apart_data_for_post=i[1], apart_data_for_put=i[2])
        if responce.json() == i[2]:
            logs.logger.debug(f'Set success for id{i[0]}')

    logs.logger.info('Starting to Deleting all of this shit')
    for apart_id in range(1, 50):
        io_object.send_request_hard(method='DELETE', api_menu='apartments', index=str(apart_id),
                                    data=None)
