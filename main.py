import requests
import base64
import argparse
import importlib
import sys

parser = argparse.ArgumentParser(description='WEB API DOMO-PHONE')
parser.add_argument('--device', help='Device configuration')
parser.add_argument('--test', help='tests to run')
args = parser.parse_known_args(sys.argv)[0]

params = args.device.split(':')

print(params)  #TODO add logs


session = requests.Session()
session.verify = False


class WebApiAdapter:
    def __init__(self, device_parameters):
        self.session = requests.Session()
        self.session.verify = False
        self.protocol = device_parameters[0]
        self.host = device_parameters[1]
        self.login = device_parameters[2]
        self.password = device_parameters[3]
        self.api_version = device_parameters[4]
        encoded_login_password = base64.b64encode(f'{self.login}:{self.password}'.encode("UTF-8")).decode("UTF-8")
        self.headers = {'Authorization': f'Basic {encoded_login_password}',
                        'Content-Type': 'application/json'}  # TODO make sure this params doesnt change

    def send_request(self, method, data, api_menu='', index=''):
        url = f'{self.protocol}://{self.host}/cgi-bin/luci/;stok=nateks/{self.login}/intercom/api/{self.api_version}/{api_menu}/{index}'
        request = self.session.request(method=method, url=url, headers=self.headers, data=data)
        return request


if __name__ == '__main__':
    io_object = WebApiAdapter(params)
    test_to_run = args.test
    iter_tools = importlib.import_module(('.' + args.test), '.tests')
    iter_tools.test_main(io_object)  # will run test_main() from imported module
