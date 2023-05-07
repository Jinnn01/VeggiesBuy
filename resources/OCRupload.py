from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
import os

blp = Blueprint("OCRupload", __name__, description="OCRUploading")


@blp.route("/ocrimage")
class OCRUpload(MethodView):
    # UPLOAD_FOLDER = '/path/to/the/uploads'
    # ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def post(self, ocrimg):
        bytesOfImage = request.get_data()
        with open('image.jpeg', 'wb') as out:
            out.write(bytesOfImage)
        return "Image read"
