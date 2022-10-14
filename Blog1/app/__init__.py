from flask import Flask, redirect
import os
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime) -%(levelname)-%(levelno) message:%(message)',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logformatter = "%(asctime) -%(levelname)-%(levelno) message:%(message)"

fapp = Flask(__name__)

filef = open("app/file/donotdel.txt", "w+")
filei = filef.read()
@fapp.route("/first/")
def firstrun():
    if int(filei) == 0:
        pass
    else:
        return redirect("/errorpage"), 404


fapp.config["SECRET_KEY"] = "ss"

import app.home.views
import app.admin.views
import app.tools.request
