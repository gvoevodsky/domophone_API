import json
import time


def change_bool(dictionary, key):  # u can play with this func
    if type(dictionary[key]) is True:
        dictionary[key] = False
    elif dictionary[key] is False:
        dictionary[key] = False
    else:
        print('ERROR', dictionary, key)


def revert_bool(
        dictionary_var):  # function go though json with level 3 nesting and changing all bool values with change_bool(dict, key)
    dictionary = dictionary_var
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
    if dictionary == dictionary_var:
        print('Nihua ne rabotaet')
    return dictionary


def test_main(io_object):
    responce = io_object.send_request(method='GET', api_menu='configuration', data=None)
    json_dict = responce.json()

    print(json_dict)
    print('-' * 100 + '\n')
    time.sleep(1)
    revert_dict = revert_bool(json_dict)
    if json_dict == revert_dict:
        print('OLOLO')
    print(revert_dict)

    time.sleep(1)
    # request = io_object.send_request(method='PUT', api_menu='configuration', data=json.dumps(revert_dict))
    # print(request.json())
    # responce  = io_object.send_request(method='GET', api_menu='configuration', data=None)
    # print(responce.json())


if __name__ == '__main__':
    dick = {'a': True, 'b': False}
    change_bool(dick, 'a')
    print(dick)
