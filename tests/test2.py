import json
import time


class BoolConfigTest:
    def __init__(self, io_object):
        self.io = io_object
        self.data = {}

    def getConfig(self):
        response = self.io.send_request(method='GET', api_menu='configuration', data=None)
        json_dict = response.json()
        print('GET №1\n', json_dict)
        self.data = json_dict
        time.sleep(1)

    def putConfig(self, data):
        print('sending reverted boolean \n')
        request = self.io.send_request(method='PUT', api_menu='configuration', data=json.dumps(data))
        print(request.json())
        time.sleep(1)

    def testBoolean(self, d: dict = {}, pathToBoolean: list = []):
        if not d:
            d = self.data
        for key, value in d.items():
            if type(value) is bool:
                self.createNestedDict([*pathToBoolean, key], not value)
            elif type(value) is dict:
                self.testBoolean(value, [*pathToBoolean, key])

    def createNestedDict(self, listOfArgs, value):
        output = originalDict = {}
        if len(listOfArgs) == 1:
            originalDict = {listOfArgs[0]: value}
        elif len(listOfArgs) > 1:
            for arg in listOfArgs[:-1]:
                output.setdefault(arg, {})
                output = output[arg]
            output[listOfArgs[-1]] = value
        self.putConfig(originalDict)


def test_main(io_object):
    test = BoolConfigTest(io_object)
    test.testBoolean()


if __name__ == '__main__':
    test_main('something')  # ?