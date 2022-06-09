# pipreqs . --encoding=utf8 --force

import model as model

import flask

App=flask.Flask(__name__)

@App.route('/')
def home():
    return 'Hello'






App.secret_key=model.tool.GetConfigData('Flask','SecretKey')
if __name__ == '__main__':
    App.run(host='127.0.0.1',port=8000,debug=True)