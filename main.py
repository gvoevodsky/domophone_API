import requests
import base64
import argparse
import importlib
import sys

parser = argparse.ArgumentParser(description='WEB API DOMO-PHONE')
parser.add_argument('--device', help='Device configuration')
parser.add_argument('--test', help='tests to run')
args = parser.parse_known_args(sys.argv)[0]

device_parameters = args.device.split(':')

print(device_parameters) #TODO add logs


session = requests.Session()
session.verify = False


class WebApiAdapter:
    def __init__(self, device_parameters):
        self.session = requests.Session()
        self.session.verify = False
        self.wproto = device_parameters[0]
        self.host = device_parameters[1]
        self.login = device_parameters[2]
        self.password = device_parameters[3]
        self.api_version = device_parameters[4]
        encoded_login_password = base64.b64encode(f'{self.login}:{self.password}'.encode("UTF-8")).decode("UTF-8")
        self.headers = {'Authorization': f'Basic {encoded_login_password}',
                        'Content-Type': 'application/json'}  # TODO make sure this params doesnt change

    def send_request(self, method, data, api_menu='', index=''):
        url = f'{self.wproto}://{self.host}/cgi-bin/luci/;stok=nateks/{self.login}/intercom/api/{self.api_version}/{api_menu}/{index}'
        request = self.session.request(method=method, url=url, headers=self.headers, data=data)
        return request


if __name__ == '__main__':
    io_object = WebApiAdapter(device_parameters)
    test_to_run = args.test
    iter_tools = importlib.import_module(('.' + args.test), '.tests')
    iter_tools.test_main(io_object)  # will run test_main() from imported module

# request3 = session.post(url=url, data=json.dumps(payload), headers=headers)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/apartments/15'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/dopen/7'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/doors/main'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/cfgftpdownload/base'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/reboot'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/configuration'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/status'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/ftp_autoupload'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/info'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/softupdate/status'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/softupdate/install'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=nateks/admin/intercom/api/v1/softupdate/download'%(wproto,host)
# url = '%s://%s/cgi-bin/luci/;stok=ccf238e0c9882c1f19620f90d082daaa/admin/intercom/api/v1/dopen/7'%(wproto,host)
# headers = {'Authorization': 'Basic YWRtaW46YWRtaW4=', 'Content-Type': 'application/json'}  # %ss autorisation
# headers = {'Cookie': 'sysauth=3f0bf96c592b86c1969ac4119e3e5e0b', 'Content-Type': 'application/json'}
# headers = {'Content-Type': 'application/json'}
