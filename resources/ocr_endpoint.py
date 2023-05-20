import json
from flask_smorest import Blueprint
from flask import request as rq
from PIL import Image

from models.ocr_implementation import *

blp = Blueprint("ocr_endpoint", __name__, description="endpoints related to ocr")

@blp.route("/ocr", methods=['POST'])
def get_ocr_text():
    image = rq.files.get('image_file')
    img_pil = Image.open(image)

    # WOOLIES
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220310_065542851.jpg"

    # coles
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220323_024424431.jpg"
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220418_081838325.jpg"

    # ALDI
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220418_053809003.jpg"
    # filename = "/Users/rohith_hb/Desktop/reciepts/PXL_20220418_053809003.jpg"

    image = preprocess(img_pil)

    text = do_ocr(image)
    text_array = text.split("\n")
    text_array = [x for x in text_array if x != '']
    output = text_analyze(text_array)
    output_json = json.dumps(output.__dict__, indent=4)
    return output_json

# text = get_ocr_text()