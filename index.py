# pipreqs . --encoding=utf8 --force

import module as module

import flask
# Init flask
App=flask.Flask(__name__)
App.config['JSON_AS_ASCII'] = False

# Init Firebase
FireBase=module.database.DB()

@App.route('/',methods=['GET','POST'])
def Home():
    return '這是臨時首頁'

@App.route('/api/TravelInfo')
def TravelInfo():
    return flask.jsonify(FireBase.Search('TravelInfo'))

@App.route('/op/Info',methods=['GET','POST'])
def Info():
    if flask.request.method=='POST':
        if flask.request.values.get('ActionType')=='CU':
            FireBase.HandleUpdateDatabase('CU','TravelInfo')
        elif flask.request.values.get('ActionType')=='D':
            FireBase.HandleUpdateDatabase('D','TravelInfo')
    return flask.render_template('Info.html')


App.config['secret_key']=module.tool.GetConfigData('Flask','SecretKey')
if __name__ == '__main__':
    App.run(host='127.0.0.1',port=8000,debug=True)