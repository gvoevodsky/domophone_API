import json
import random
import logs
import random_gen


def test_main(io_object):
    all_data = io_object.send_request_hard(method='GET', api_menu='status', pretty=True)

    sip_reg_data = io_object.send_request_hard(method='GET', api_menu='status', index='sip_reg')

    display_data = io_object.send_request_hard(method='GET', api_menu='status', index='display')

    sysinfo_data = io_object.send_request_hard(method='GET', api_menu='status', index='sysinfo')

    dic = display_data.json()['response']
    dic['display']['text'] = random_gen.get_random_string(1, 50, 'abcdefghijklmnopqrstuvwxyz1234567890')
    dic['display']['speed'] = random.choice('12345')

    io_object.send_request_hard(method='PUT', api_menu='status', data=json.dumps(dic))

    new_display_data = io_object.send_request_hard(method='GET', api_menu='status', index='display')

    a = new_display_data.json()['response']
    if a == dic: #dict are not comparable
        logs.logger.info('success')
    else:
        logs.logger.info('ne success')
