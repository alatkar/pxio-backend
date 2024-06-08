from . import app
from flask import request

@app.route("/rfps/<rfpid>/chat")
def getRfp(rfpid=None):
    return {"Response": "LLM Generated Response for RFP " + rfpid}

