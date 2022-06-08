from flask import Flask, jsonify, render_template,make_response
from controller.recupdata import *

app=Flask(__name__)



@app.route("/")
def index():
    dic={
        "Macky Sall": 58,
        "Idrissa Seck":20,
        "Ousmane Sonko": 15
    }
    donne=RecupElecteur()
    return render_template('index.html',donne=donne,dic=dic)



@app.route("/bureaucom")
def data():
    data=BureauCom()
    return jsonify(data)

@app.route("/nbrcommuneregion")
def datacom():
    data=RecupNbrCommune()
    return jsonify(data)

@app.route("/datalieu")
def datalieu():
    datalieuvote=recupBureauVote()
    return jsonify(datalieuvote)

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'Page indisponible'
    return resp



if __name__=='__main__':
    app.run(debug=True) 