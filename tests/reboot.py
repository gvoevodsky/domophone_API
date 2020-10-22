import logs

def test_main(io_object):
    logs.logger.info('Sending Reboot command')
    io_object.send_request_hard(method='POST', api_menu='reboot')