import json
import random

import logs


def test_main(io_object):
    logs.logger.info('Test doors started')
    all_doors = [i for i in range(8)]
    all_doors.append('main')
    logs.logger.debug(all_doors)

    door_id = 5

    io_object.send_request_hard(method='POST', api_menu='dopen', index='main')   # коротковременное открытие двери н                                    # влияет на GET её состояния

    io_object.send_request_hard(method='GET', api_menu='doors', index='main')

    io_object.send_request_hard(method='POST', api_menu='dopen', index=str(door_id))

    io_object.send_request_hard(method='GET', api_menu='doors', index=str(door_id))

    result_data = {}
    for door_id in all_doors:
        data = {"state": random.choice([0, 1])}
        result_data[str(door_id)] = data

        io_object.send_request_hard(method='GET', api_menu='doors', index=str(door_id),
                                    data=None)

        io_object.send_request_hard(method='PUT', api_menu='doors', index=str(door_id),
                                    data=json.dumps(data))

        io_object.send_request_hard(method='GET', api_menu='doors', index=str(door_id),
                                    data=None)

    r = io_object.send_request_hard(method='GET', api_menu='doors',
                                    data=None, pretty=True)
    response = r.json()['response']
    if response == result_data:
        logs.logger.info('Test succeed')
    else:
        logs.logger.info('Test failed')
    return True
