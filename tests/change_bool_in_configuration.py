import json
import time


def change_bool(dictionary, key):  # u can play with this func
    if dictionary[key] is True:
        dictionary[key] = False
    elif dictionary[key] is False:
        dictionary[key] = True
    else:
        print('ERROR', dictionary, key)
    return dictionary[key]


def send_put_request(io_object, api_menu, data_to_send):
    request = io_object.send_request_hard(method='PUT', api_menu=api_menu,
                                          data=json.dumps(data_to_send))
    print(data_to_send, '-' * 5, request.json(), '-' * 5, request.status_code)

    # request = io_object.send_request(method='GET', api_menu=api_menu, TODO придумать как отправлять запрос GET и проверять изменение, потому что WEB API жрет все
    #                                data=None)
    # print(data_to_send, request.json())


def revert_bool_recoursion(io_object, dictionary, key_path=[], api_menu='configuration'):
    for key, value in dictionary.items():
        if type(value) is dict:
            key_path.append(key)
            revert_bool_recoursion(io_object, dictionary[key], key_path, api_menu)
            key_path.pop()

        elif type(value) is bool:
            new_value = change_bool(dictionary, key)
            full_path = {key: new_value}
            for path_key in key_path[::-1]:
                full_path = {path_key: full_path}
            send_put_request(io_object=io_object, api_menu=api_menu, data_to_send=full_path)
            time.sleep(0.5)
        elif type(value) is list:
            pass  # TODO придумать что делать со строками и списками
        elif type(value) is str:
            pass
        else:
            pass


def revert_bool_best(dic):
    list_of_values = []
    list_of_dicts = []
    while list_of_dicts is True:
        for key, value in dic.items():
            if type(value) is dict:
                list_of_dicts.append(value)
            else:
                list_of_values.append({key: value})


def test_main(io_object):
    response = io_object.send_request_hard(method='GET', api_menu='configuration', data=None)
    json_dict = response.json()['response']
    print(json_dict)
    print(type(json_dict))

    revert_bool_recoursion(io_object, json_dict, api_menu='configuration')

    response = io_object.send_request_hard(method='GET', api_menu='configuration', data=None)
    json_dict = response.json()
    print(json_dict)
