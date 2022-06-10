# pipreqs . --encoding=utf8 --force

import module as module

import flask
# Init flask
App=flask.Flask(__name__)
App.config['JSON_AS_ASCII'] = False

# Init Firebase
FireBase=module.database.DB()

@App.route('/')
def Home():
    return '這是臨時首頁'

@App.route('/api/TravelInfo')
def TravelInfo():
    return flask.jsonify(FireBase.STravelInfo())

@App.route('/op/CUInfo',methods=['GET',"POST"])
def CUInfo():
    if flask.request.method=='POST':
        FireBase.FormDataGet('CU')
    return flask.render_template('CUInfo.html')

App.config['secret_key']=module.tool.GetConfigData('Flask','SecretKey')
if __name__ == '__main__':
    App.run(host='127.0.0.1',port=8000,debug=True)