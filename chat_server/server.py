from tornado import ioloop, web, websocket, escape
from datetime import datetime
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
distdir = os.path.join(basedir, 'chat_web/dist')


class ChatSocket(websocket.WebSocketHandler):
    pool = set()

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        ChatSocket.pool.add(self)
        logger.info('{}: websocket open'.format(self.request.host))

    def on_message(self, message):
        # print(message)
        message = escape.json_decode(message)
        if message['uid'] and message['msg']:
            ChatSocket.update({
                'uid': message['uid'],
                'msg': message['msg'],
                'time': datetime.now().strftime('%m-%d %H:%M:%S')
            })

    def on_close(self):
        ChatSocket.pool.remove(self)
        logger.info('{}: websocket close'.format(self.request.host))

    def send_error(self, *args, **kwargs):
        # self.write_message('send_error')
        logger.error('{}: websocket send error, msg: {}, {}'.format(
            self.request.host,
            args,
            kwargs
        ))

    def write_error(self, status_code, **kwargs):
        logger.error('{}: websocket write error, status_code: {}, msg: {}'.format(
            self.request.host,
            status_code,
            kwargs
        ))

    @classmethod
    def update(cls, msg):
        for item in cls.pool:
            item.write_message(msg)


class ChatWebHandel(web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def get(self, *args, **kwargs):
        self.render(distdir + '/index.html')

    def post(self, *args, **kwargs):
        # uid = self.get_argument('uid', None)
        # hashid = self.create_signed_value('uid', uid)
        # if uid:
        #     self.write({'hashid': str(hashid)})
        pass

route = [
    (r'/chatws', ChatSocket),
    (r'/chat', ChatWebHandel)
]


def make_app():
    return web.Application(route, static_path=distdir + '/static')


if __name__ == '__main__':
    app = make_app()
    app.listen(80)
    ioloop.IOLoop.current().start()