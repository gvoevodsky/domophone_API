def test_main(io_object):
    while True:
        io_object.send_request_hard(method='GET', api_menu='apartments', index=str(1),
                                    data=None)
