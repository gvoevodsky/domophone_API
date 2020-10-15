import argparse
import base64
import importlib
import sys
import time

import requests

import logs

parser = argparse.ArgumentParser(description='WEB API DOMO-PHONE')
parser.add_argument('--device', help='Device configuration')
parser.add_argument('--test', help='tests to run')
args = parser.parse_known_args(sys.argv)[0]

params = args.device.split(':')

logs.logger.debug(params)
logs.logger.debug('-' * 100)

session = requests.Session()
session.verify = False


class WebApiAdapter:
    """
    Parser examples:
    --device http:192.168.8.254:admin:admin:v1 --create_and_check_apartment
    --device http:192.168.8.254:admin:admin:v1 --test get_to_apartments
    --device http:192.168.8.254:admin:admin:v1 --test change_bool_in_configuration
    """

    def __init__(self, device_parameters):
        self.session = requests.Session()
        self.session.verify = False
        self.protocol = device_parameters[0]
        self.host = device_parameters[1]
        self.login = device_parameters[2]
        self.password = device_parameters[3]
        self.api_version = device_parameters[4]
        self.encoded_login_password = base64.b64encode(f'{self.login}:{self.password}'.encode("UTF-8")).decode("UTF-8")
        self.headers = {'Authorization': f'Basic {self.encoded_login_password}',
                        'Content-Type': 'application/json'}  # TODO make sure this params doesnt change

    def send_request(self, method, data, api_menu='', index=''):
        """
        :param method: GET, POST, PUT, DELETE
        :param data: Json dict or None
        :param api_menu: 'configuration' or another
        :param index:
        :return: response json, if json is empty returns request status code
        """
        url = f'{self.protocol}://{self.host}/cgi-bin/luci/;stok=nateks/{self.login}/intercom/api/{self.api_version}/{api_menu}/{index}'
        request = self.session.request(method=method, url=url, headers=self.headers, data=data)
        logs.logger.debug(f'{method}/{api_menu}/{index}:   ')
        if request.status_code in [200, 201, 202,
                                   203]:  # TODO нужен более правильный метод обработки пустых ответов с сервера
            logs.logger.debug(request)
            logs.logger.debug(request.json())
        else:
            logs.logger.debug(request)
        return request

    def send_request_hard_demo(self, method, data, api_menu='', index=''):  # TODO доделать метод
        try:
            responce = self.send_request(method, data, api_menu='', index='')
        except requests.exceptions.ChunkedEncodingError:
            try:
                logs.logger.warning(
                    f'FIRST ChunkedEncodingError for method:{method} , {api_menu}/{index}')
                time.sleep(1)
                responce = self.send_request(method, data, api_menu='', index='')
            except requests.exceptions.ChunkedEncodingError:
                logs.logger.error(
                    f'SECOND ChunkedEncodingError for method:{method} , {api_menu}/{index}')
                self.session = requests.Session()
                self.session.verify = False
                time.sleep(10)
                responce = self.send_request(method, data, api_menu='', index='')
        return responce

    def send_request_hard(self, method, data, api_menu='', index=''):
        """
        Same as send_request, but checking response for ChunkedEncodingError, if it raises send same request.
        :param method:
        :param data:
        :param api_menu:
        :param index:
        :return:
        """
        url = f'{self.protocol}://{self.host}/cgi-bin/luci/;stok=nateks/{self.login}/intercom/api/{self.api_version}/{api_menu}/{index}'
        try:
            request = self.session.request(method=method, url=url, headers=self.headers, data=data)
        except requests.exceptions.ChunkedEncodingError:
            logs.logger.warning(f'ChunkedEncodingError for method:{method} , {api_menu}/{index}')
            time.sleep(5)
            request = self.session.request(method=method, url=url, headers=self.headers, data=data)
        logs.logger.debug(f'{method}/{api_menu}/{index}:   ')
        if request.status_code in [200, 201, 202,
                                   203]:  # TODO нужен более правильный метод обработки пустых ответов с сервера
            logs.logger.debug(request)
            logs.logger.debug(request.json())
        else:
            logs.logger.debug(request)
        return request


if __name__ == '__main__':
    io_object = WebApiAdapter(params)
    test_to_run = args.test
    iter_tools = importlib.import_module(('.' + args.test), '.tests')
    iter_tools.test_main(io_object)  # will run test_main() from imported module
