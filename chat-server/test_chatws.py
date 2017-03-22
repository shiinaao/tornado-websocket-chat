from .server import make_app
from tornado.testing import AsyncHTTPTestCase, gen_test, main
from tornado.websocket import websocket_connect
from tornado import escape


class ChatWebSocketTest(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()


    @gen_test
    def test_chatws(self):
        ws = yield websocket_connect('ws://127.0.0.1:{}/chatws'.format(self.get_http_port()), io_loop=self.io_loop)
        # res = yield ws.read_message()
        # self.assertTrue(res == 'Connected')

        ws.write_message(escape.json_encode({'msg': '12 login', 'uid': '12'}))
        res = yield ws.read_message()
        self.assertIn('12', res)


if __name__ == '__main__':
    main()