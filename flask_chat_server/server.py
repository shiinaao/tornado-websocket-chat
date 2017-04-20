from flask import Flask ,render_template
from flask_socketio import SocketIO, Namespace, send
import os
# import logging
#
# logger = logging.getLogger()
# log_level = os.environ.get('log_level').upper()
# logger.setLevel(getattr(logging, log_level))

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
distdir = os.path.join(basedir, 'chat_web/dist')


app = Flask(__name__, static_folder=distdir)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)



@app.route('/chat')
def chat_page():
    render_template(distdir+'/index.html')


class ChatWebSocket(Namespace):
    # namespace = 'chatws'

    def on_connect(self):
        print('login')

    def on_disconnect(self):
        print('logout')

    def on_message(self, data):
        send(data, json=True, broadcast=True)


    # def handle_bc(self, data):

socketio.on_namespace(ChatWebSocket('/chatws'))