from flask import Flask, request
from PIL import Image
import json, io, os
import logging

log = logging.getLogger("mahalovo")
log.level = logging.INFO
log.info("[...] Starting PoseML")

log.info("[...] Pose recognizer...")
from pose import get_pose
log.info("[...] Catboost model...")
from cb_model import get_catboost_pred, catboost_models
log.info("[...] logreg model...")
from lg_model import get_logreg_pred, logreg_models
log.info("[+++] Complete! Starting server.")

app = Flask("mahalovo")

def logreg_categorize(image):
    pred, acc = get_logreg_pred(image, logreg_models[0])
    # TODO: Add logreg implementation here
    log.info(f"[LogReg] Predicted {pred} with P={acc} !")
    return (pred, acc)

def catboost_categorize(image):
    pred, acc = get_catboost_pred(image, catboost_models[1])
    log.info(f"[Catboost] Predicted {pred} with P={acc} !")
    return (pred, acc)

categorize = logreg_categorize

@app.route('/')
def index():
    return open("static/index.html", "r").read()

@app.route("/api/recognize", methods=["POST"])
def recognize():
    raw_image = request.files["image"].read()
    image = Image.open(io.BytesIO(raw_image))
    pred, acc = categorize(image)
    return json.dumps({"pred": pred, "acc": acc})

app.run(host='0.0.0.0', port=8080)

