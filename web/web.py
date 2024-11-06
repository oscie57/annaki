from web import web_blueprint
import config
import requests
import python_weather

from flask import request, render_template

@web_blueprint.route('/web/')
def root():
    return render_template("welcome.html")

@web_blueprint.route('/web/acdp')
def acdp():
    return render_template("acdp.html")
