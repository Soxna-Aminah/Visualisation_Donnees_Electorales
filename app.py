from flask import Flask, jsonify, redirect, render_template,make_response
from controller.recupdata import *
from controller.recupdata import data as mydata

app=Flask(__name__)



@app.route("/")
def index():
    return render_template("home.html")

@app.route("/load",methods=["GET"])
def post():
    chargeDonnees(mydata)
    return redirect("/dashbord")

   

@app.route("/dashbord")
def dashbord():
    dic = {
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


@app.route('/api/info')
def getter_info():
    results = []
    results = getter_info_controller()
    return jsonify(results)




@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'Page indisponible'
    return resp



if __name__=='__main__':
    app.run(debug=True) 