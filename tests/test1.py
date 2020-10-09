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

def revert_bool(dictionary_var):  # function go though json with level 3 nesting
    dictionary = dictionary_var  # and changing all bool values with change_bool(dict, key)
    for key_1, value_1 in dictionary.items():
        if type(value_1) is dict:
            for key_2, value_2 in dictionary[key_1].items():
                if type(value_2) is dict:
                    for key_3, value_3 in dictionary[key_1][key_2].items():
                        if type(value_3) is dict:
                            for key_4, value_4 in dictionary[key_1][key_2][key_3].items():
                                if type(value_4) is bool:
                                    change_bool(dictionary[key_1][key_2][key_3], key_4)
                                else:
                                    pass
                        elif type(value_3) is bool:
                            change_bool(dictionary[key_1][key_2], key_3)
                        else:
                            pass

                elif type(value_2) is bool:
                    change_bool(dictionary[key_1], key_2)
                else:
                    pass
        else:  # systems keys: error and response
            pass
    return dictionary

def send_put_request(io_object, api_menu, data_to_send):
    request = io_object.send_request(method='PUT', api_menu=api_menu,
                                     data=json.dumps(data_to_send))
    print(data_to_send, request.json())


def revert_bool_recoursion(io_object, dictionary, keypath=[], api_menu='configuration'):
    for key, value in dictionary.items():
        if type(value) is dict:
            keypath.append(key)
            revert_bool_recoursion(io_object, dictionary[key], keypath, api_menu)
            keypath.pop()

        elif type(value) is bool:
            new_value = change_bool(dictionary, key)
            fullPath = {key : new_value}
            for pathKey in keypath[::-1]:
                fullPath = {pathKey: fullPath}
            send_put_request(io_object=io_object, api_menu=api_menu, data_to_send=fullPath)
        else:
            pass

def test_main(io_object):
    response = io_object.send_request(method='GET', api_menu='configuration', data=None)
    json_dict = response.json()['response']
    print(json_dict)
    print(type(json_dict))

    revert_bool_recoursion(io_object, json_dict, api_menu='configuration')


    response = io_object.send_request(method='GET', api_menu='configuration', data=None)
    json_dict = response.json()
    print(json_dict)
