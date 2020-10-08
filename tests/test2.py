import json
import time


def change_bool(dictionary, key, io_object):  # u can play with this func
    if dictionary[key] is True:
        dictionary[key] = False
    elif dictionary[key] is False:
        dictionary[key] = True
    else:
        print('ERROR', dictionary, key)
    request = io_object.send_request(method='PUT', api_menu='configuration', data=json.dumps(dictionary[key]))
    print(request.json())

def wtf():




def test_main(io_object):
    response = io_object.send_request(method='GET', api_menu='configuration', data=None)
    dictionary = response.json()
    for key_1, value_1 in dictionary.items():
        if type(value_1) is dict:
            for key_2, value_2 in dictionary[key_1].items():
                if type(value_2) is dict:
                    for key_3, value_3 in dictionary[key_1][key_2].items():
                        if type(value_3) is dict:
                            for key_4, value_4 in dictionary[key_1][key_2][key_3].items():
                                if type(value_4) is bool:
                                    sting = f'{key_1}:{'{}'' #TODO придумать как сгенерить словарь с единственным значением.
                                    ebanutii_dict = { key_1 : {key_2 : key_3}}


                                    change_bool(dictionary[key_1][key_2][key_3], key_4, io_object)
                                else:
                                    pass
                        elif type(value_3) is bool:
                            change_bool(dictionary[key_1][key_2], key_3, io_object)
                        else:
                            pass

                elif type(value_2) is bool:
                    change_bool(dictionary[key_1], key_2, io_object)
                else:
                    pass
        else:  # systems keys: error and response
            pass
    return dictionary























    response = io_object.send_request(method='GET', api_menu='configuration', data=None)
    json_dict = response.json()
    print('GET №1\n', json_dict)
    time.sleep(1)

    revert_dict = revert_bool(json_dict)
    print('reverted\n', revert_dict)
    time.sleep(1)

    print('sending reverted boolean \n')
    request = io_object.send_request(method='PUT', api_menu='configuration', data=json.dumps(revert_dict['response']))
    print(request.json())

    print('GET №2\n')
    response = io_object.send_request(method='GET', api_menu='configuration', data=None)
    print('server response:\n')
    print(response.json())


if __name__ == '__main__':
    test_main('something') #?
