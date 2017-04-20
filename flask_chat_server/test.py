from .server import socketio, app
from flask_socketio import SocketIOTestClient
import unittest


class FlaskWebSocketTest(unittest.TestCase):
    def setUp(self):
        self.ws = SocketIOTestClient(app, socketio)
        self.ws.connect(namespace='/chatws')


    def test_ws(self):
        self.assertTrue(self.ws)
        self.ws2 = SocketIOTestClient(app, socketio, namespace='/chatws')
        self.ws2.send('i am ws2', namespace='/chatws')
        rev = self.ws.get_received(namespace='/chatws')
        self.assertEqual(rev[0]['args'], 'i am ws2')

    def tearDown(self):
        self.ws.disconnect()


if __name__ == '__main__':
    unittest.main()